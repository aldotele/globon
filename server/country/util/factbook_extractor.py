import re


class FactbookExtractor:
    @staticmethod
    def extract_field(json, *subfields):
        res = json
        for subfield in subfields:
            try:
                res = res[subfield]
            except KeyError:
                return None
        return res

    @staticmethod
    def extract_population(string):
        if len(string) > 0 and string[0].isdigit() and " (" in string:
            number = string.split(" (")[0].replace(",", "")
            return int(number)
        return None

    @staticmethod
    def extract_capital(json, subfields):
        capital_string = FactbookExtractor.extract_field(json, *subfields)
        if capital_string:
            capital_string_split = capital_string.split("; ")

        # TODO update capital retrieval, sometimes there are sentences
            return [capital[:capital.index(" (")] if " (" in capital
                    else capital for capital in capital_string_split if "note" not in capital]
        return None

    @staticmethod
    def extract_coordinates(json, subfields):
        try:
            input = FactbookExtractor.extract_field(json, *subfields)
            if not input:
                return None
            # separate latitude text from longitude text
            split = input.split(", ")
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
    def extract_area(json, subfields):
        area_string = FactbookExtractor.extract_field(json, *subfields)
        if area_string and " sq" in area_string:
            area_string_split = area_string.split(" sq")
            number_part = area_string_split[0].replace(",", "")
            if number_part.isdigit():
                return int(number_part)
        return None

    @staticmethod
    def extract_length(json, subfields):
        length_string = FactbookExtractor.extract_field(json, *subfields)
        if length_string and " km" in length_string:
            length_string_split = length_string.split(" km")
            number_part = length_string_split[0].replace(",", "")
            if number_part.isdecimal():
                return float(number_part)
        return None

    @staticmethod
    def extract_border_countries(json, subfields):
        res = {}
        border_countries_string = FactbookExtractor.extract_field(json, *subfields)
        if border_countries_string:
            border_countries_string = border_countries_string.split(";")
            for el in border_countries_string:
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
