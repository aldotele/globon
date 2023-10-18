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
    def extract_flag(gec):
        return "https://www.cia.gov/the-world-factbook/static/flags/" + gec.upper() + "-flag.jpg"

    @staticmethod
    def extract_map(gec):
        return "https://www.cia.gov/the-world-factbook/static/maps/" + gec.upper() + "-map.jpg"
