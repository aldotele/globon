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
        # TODO implement extraction and conversion of coordinates
        return FactbookExtractor.extract_field(json, *subfields)

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

