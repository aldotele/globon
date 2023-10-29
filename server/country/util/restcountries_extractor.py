class RestcountriesExtractor:

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
    def extract_translations(json_node):
        translations = []
        for key, value in json_node.items():
            translation = value['common']
            if translation not in translations:
                translations.append(translation)
        return translations

    @staticmethod
    def extract_currencies(json_node):
        currencies = []
        for key, value in json_node.items():
            currency = value.get('name', "")
            if 'symbol' in value:
                currency += " (" + value['symbol'] + ")"
            currencies.append(currency)
        return currencies

    @staticmethod
    def extract_languages(json_node):
        languages = []
        for key, value in json_node.items():
            languages.append(value)
        return languages


if __name__ == '__main__':
    json_node = {"a": {"b": {"c": 15}}}
    print(RestcountriesExtractor.extract_field(json_node, "a", "b", "cs"))
