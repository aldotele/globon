import locale
import re


class FactbookExtractor:
    @staticmethod
    def extract_field(json, *subfields) -> str | dict | None:
        res = json
        for subfield in subfields:
            try:
                res = res[subfield]
            except KeyError:
                return None
        return res

    @staticmethod
    def extract_by(text: str, delimiters=(), until="", after="", pattern=None):
        if text and delimiters:
            index_of_start = text.index(delimiters[0]) if delimiters[0] in text else None
            index_of_end = text.index(delimiters[1]) if delimiters[1] in text else None
            return text[index_of_start + 1:index_of_end] if None not in (index_of_start, index_of_end) else None
        elif text and until:
            return text[:text.index(until)] if until in text else None
        elif text and after:
            return text[text.index(after) + 1:] if after in text else None
        elif text and pattern:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

    @staticmethod
    def parse_number(text: str):
        if text:
            try:
                return locale.atof(text)
            except ValueError:
                # might insert a log to keep track of not parsed elements
                return None

    @staticmethod
    def extract_capital(json, *subfields):
        capital_text = FactbookExtractor.extract_field(json, *subfields)
        if not capital_text:
            return None
        # splitting by ; which divides capitals in case of more capitals
        capital_text_split = capital_text.split("; ")
        # ignoring the parentheses notes if present
        extracted = [capital[:capital.index(" (")] if " (" in capital
                     else capital for capital in capital_text_split if "note" not in capital]
        # handle case of more elements with possible notes/sentences in it
        if len(extracted) > 1:
            # variable that will store actual capitals, leaving out notes and sentences
            kept = [extracted[0]]
            # the check will start from the second element as the first one is always a capital for sure
            for element in extracted[1:]:
                # element is considered a capital if every word starts with uppercase
                if all(word[0].isupper() for word in element.split(" ")):
                    kept.append(element)
            return kept
        else:
            return extracted

    @staticmethod
    def extract_coordinates(json, *subfields):
        try:
            coordinates_text = FactbookExtractor.extract_field(json, *subfields)
            if not coordinates_text:
                return None
            # separate latitude text from longitude text
            split = coordinates_text.split(", ")
            # the pattern to extract, namely a pattern that match the format like "13 50 N" or "3 5 N"
            pattern = r'\d{1,2}\s\d{1,2}\s[A-Z]'

            if len(split) >= 2:
                match_on_lat = re.search(pattern, split[0])
                if not match_on_lat:
                    return None
                lat_text = match_on_lat.group()

                match_on_lng = re.search(pattern, split[1])
                if not match_on_lng:
                    return None
                lng_text = match_on_lng.group()

                lat_split = lat_text.split(" ")
                lng_split = lng_text.split(" ")

                if len(lat_split) >= 3 and len(lng_split) >= 3:
                    # first part is the degrees of latitude and longitude
                    lat_result = lat_split[0]
                    lng_result = lng_split[0]

                    # divide the number of minutes by 60 to convert them to decimal degrees
                    # for example if input for latitude is "15 30 S", 30 divided by 60 is 0.5 that will be added to 15
                    if lat_split[1] != "00":
                        lat_result = str(int(lat_result) + int(lat_split[1]) / 60)
                    if lng_split[1] != "00":
                        lng_result = str(int(lng_result) + int(lng_split[1]) / 60)

                    # for South and West the result becomes negative
                    lat_result = lat_result if "N" in lat_split[2] else "-" + lat_result
                    lng_result = lng_result if "E" in lng_split[2] else "-" + lng_result

                    return [float(lat_result), float(lng_result)]

                else:
                    return None
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def extract_border_countries(json, *subfields):
        res = {}
        border_countries_text = FactbookExtractor.extract_field(json, *subfields)
        if border_countries_text:
            border_countries_text = border_countries_text.split(";")
            for el in border_countries_text:
                match = re.search(r'^(.*?)(\d+)', el)
                if match:
                    country = match.group(1).strip()
                    length = match.group(2).strip()
                    res[country] = int(length)
        return res

    @staticmethod
    def extract_flag(gec):
        return "https://www.cia.gov/the-world-factbook/static/flags/" + gec.upper() + "-flag.jpg"

    @staticmethod
    def extract_map(gec):
        return "https://www.cia.gov/the-world-factbook/static/maps/" + gec.upper() + "-map.jpg"

    @staticmethod
    def extract_official_languages(json):
        # TODO way to standardize extraction
        attempt_1 = FactbookExtractor.extract_field(json, *['People and Society', 'Languages', 'Languages', 'text'])
        attempt_2 = FactbookExtractor.extract_field(json, *['People and Society', 'Languages', 'text'])
        regexp = re.findall(r'\w+(?=\s*\(official)', attempt_1)
        return None


    @staticmethod
    def extract_until_delimiter(json, delimiter, *subfields):
        extracted = FactbookExtractor.extract_field(json, *subfields)
        if not extracted:
            return None
        return locale.atof(extracted[:extracted.index(delimiter)].strip()) \
            if delimiter in extracted.lower() else None

    @staticmethod
    def extract_most_recent_until_delimiter(json, delimiter, *subfields):
        extracted = FactbookExtractor.extract_field(json, *subfields)
        if not extracted:
            return None
        years = [int(key.split(" ")[-1]) for key in extracted.keys()
                 if (" " in key and key.split(" ")[-1].isdigit())]
        years.sort(reverse=True)
        if years:
            return FactbookExtractor.extract_until_delimiter(extracted, delimiter,
                                                             subfields[-1] + " " + str(years[0]), "text")


    @staticmethod
    def extract_gdp_real(json, *subfields):
        extracted = FactbookExtractor.extract_field(json, *subfields)
        if not extracted:
            return None
        years = [int(key.split(" ")[-1]) for key in extracted.keys()
                 if (" " in key and key.split(" ")[-1].isdigit())]
        years.sort(reverse=True)
        if years:
            extracted = FactbookExtractor.extract_field(extracted, subfields[-1] + " " + str(years[0]), "text")
            if not extracted:
                return None
            index_of_currency = extracted.index("$")
            index_of_whitespace_after_currency = extracted[index_of_currency:].index(" ")
            number_piece = extracted[index_of_currency+1:index_of_whitespace_after_currency].strip()
            if "million" in extracted:
                return locale.atof(number_piece) * 1000000
            elif "billion" in extracted:
                return locale.atof(number_piece) * 1000000000
            elif "trillion" in extracted:
                return locale.atof(number_piece) * 1000000000000
            else:
                return locale.atof(number_piece)
        return None


