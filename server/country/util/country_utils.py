class CountryUtils:
    restcountries_iso3 = ['PYF', 'MAF', 'VEN', 'REU', 'SLV', 'DMA', 'GIB', 'KEN', 'BRA', 'MDV', 'USA', 'COK', 'NIU', 'SYC', 'CAF', 'TKL', 'VUT', 'GMB', 'GUY', 'FLK', 'BEL', 'ESH', 'TUR', 'VCT', 'PAK', 'ALA', 'IRN', 'IDN', 'NZL', 'AFG', 'GUM', 'ALB', 'COD', 'CIV', 'SDN', 'TLS', 'LUX', 'SAU', 'KHM', 'NPL', 'GUF', 'MYS', 'RWA', 'THA', 'ATA', 'JOR', 'CHE', 'COM', 'UNK', 'IMN', 'MNE', 'HKG', 'JEY', 'TJK', 'BGR', 'EGY', 'MWI', 'CPV', 'BEN', 'MAR', 'IRL', 'MDA', 'DNK', 'TKM', 'FSM', 'MCO', 'BRB', 'DZA', 'ATF', 'ERI', 'LSO', 'TZA', 'MLI', 'NER', 'AND', 'GBR', 'DEU', 'VIR', 'SOM', 'SXM', 'CMR', 'DOM', 'GIN', 'NAM', 'MSR', 'SGS', 'SEN', 'BVT', 'SLB', 'FRA', 'SHN', 'MAC', 'ARG', 'BIH', 'AIA', 'GGY', 'DJI', 'KNA', 'SYR', 'PRI', 'PER', 'SMR', 'AUS', 'NCL', 'JAM', 'KAZ', 'SLE', 'PLW', 'KOR', 'SPM', 'BLZ', 'PNG', 'ISL', 'ASM', 'BFA', 'PRT', 'TWN', 'JPN', 'CHN', 'LBN', 'LKA', 'GTM', 'SRB', 'MDG', 'SWZ', 'ROU', 'ATG', 'CUW', 'ZMB', 'ZWE', 'TUN', 'ARE', 'MNG', 'NOR', 'GRL', 'URY', 'BHS', 'RUS', 'VGB', 'WLF', 'TCD', 'LCA', 'YEM', 'UMI', 'SWE', 'SJM', 'LAO', 'LVA', 'COL', 'GRD', 'BLM', 'CAN', 'HMD', 'IND', 'GNB', 'MKD', 'PRY', 'HRV', 'CRI', 'UGA', 'BES', 'BOL', 'TGO', 'MYT', 'MHL', 'PRK', 'NLD', 'IOT', 'MLT', 'MUS', 'NFK', 'HND', 'ESP', 'EST', 'KGZ', 'CHL', 'BMU', 'GNQ', 'LBR', 'PCN', 'LBY', 'LIE', 'VAT', 'CXR', 'OMN', 'PHL', 'POL', 'FRO', 'BHR', 'BLR', 'SVN', 'GLP', 'QAT', 'VNM', 'MRT', 'SGP', 'GEO', 'BDI', 'NRU', 'SSD', 'WSM', 'CCK', 'COG', 'CYP', 'KWT', 'TTO', 'TUV', 'AGO', 'TON', 'GRC', 'MOZ', 'MMR', 'AUT', 'ETH', 'MTQ', 'AZE', 'UZB', 'BGD', 'ARM', 'NGA', 'ZAF', 'BRN', 'ITA', 'FIN', 'ISR', 'ABW', 'NIC', 'HTI', 'KIR', 'TCA', 'CYM', 'UKR', 'MEX', 'PSE', 'FJI', 'SVK', 'GHA', 'SUR', 'CUB', 'BTN', 'HUN', 'STP', 'IRQ', 'CZE', 'LTU', 'MNP', 'BWA', 'PAN', 'GAB', 'ECU']
    factbook_gec = ['ag', 'ao', 'bc', 'bn', 'by', 'cd', 'cf', 'cg', 'cm', 'cn', 'ct', 'cv', 'dj', 'eg', 'ek', 'er', 'et', 'ga', 'gb', 'gh', 'gv', 'iv', 'ke', 'li', 'lt', 'ly', 'ma', 'mi', 'ml', 'mo', 'mp', 'mr', 'mz', 'ng', 'ni', 'od', 'pu', 'rw', 'se', 'sf', 'sg', 'sh', 'sl', 'so', 'su', 'to', 'tp', 'ts', 'tz', 'ug', 'uv', 'wa', 'wi', 'wz', 'za', 'zi', 'ay', 'bv', 'fs', 'hm', 'aq', 'as', 'at', 'bp', 'ck', 'cq', 'cr', 'cw', 'fj', 'fm', 'fp', 'gq', 'kr', 'kt', 'nc', 'ne', 'nf', 'nh', 'nr', 'nz', 'pc', 'ps', 'rm', 'tl', 'tn', 'tv', 'um', 'wf', 'wq', 'ws', 'aa', 'ac', 'av', 'bb', 'bf', 'bh', 'bq', 'cj', 'cs', 'cu', 'do', 'dr', 'es', 'gj', 'gt', 'ha', 'ho', 'jm', 'mh', 'nn', 'nu', 'pm', 'rn', 'rq', 'sc', 'st', 'tb', 'td', 'tk', 'uc', 'vc', 'vi', 'vq', 'kg', 'kz', 'rs', 'ti', 'tx', 'uz', 'bm', 'bx', 'cb', 'ch', 'hk', 'id', 'ja', 'kn', 'ks', 'la', 'mc', 'mg', 'my', 'pf', 'pg', 'pp', 'rp', 'sn', 'th', 'tt', 'tw', 'vm', 'al', 'an', 'au', 'ax', 'be', 'bk', 'bo', 'bu', 'cy', 'da', 'dx', 'ei', 'en', 'ez', 'fi', 'fo', 'fr', 'gi', 'gk', 'gm', 'gr', 'hr', 'hu', 'ic', 'im', 'it', 'je', 'jn', 'kv', 'lg', 'lh', 'lo', 'ls', 'lu', 'md', 'mj', 'mk', 'mn', 'mt', 'nl', 'no', 'pl', 'po', 'ri', 'ro', 'si', 'sm', 'sp', 'sv', 'sw', 'sz', 'uk', 'up', 'vt', 'ae', 'aj', 'am', 'ba', 'gg', 'gz', 'ir', 'is', 'iz', 'jo', 'ku', 'le', 'mu', 'qa', 'sa', 'sy', 'tu', 'we', 'ym', 'bd', 'ca', 'gl', 'ip', 'mx', 'sb', 'us', 'ar', 'bl', 'br', 'ci', 'co', 'ec', 'fk', 'gy', 'ns', 'pa', 'pe', 'sx', 'uy', 've', 'af', 'bg', 'bt', 'ce', 'in', 'io', 'mv', 'np', 'pk']

    gec_to_continent = {
        "ag": "africa",
        "ao": "africa",
        "bc": "africa",
        "bn": "africa",
        "by": "africa",
        "cd": "africa",
        "cf": "africa",
        "cg": "africa",
        "cm": "africa",
        "cn": "africa",
        "ct": "africa",
        "cv": "africa",
        "dj": "africa",
        "eg": "africa",
        "ek": "africa",
        "er": "africa",
        "et": "africa",
        "ga": "africa",
        "gb": "africa",
        "gh": "africa",
        "gv": "africa",
        "iv": "africa",
        "ke": "africa",
        "li": "africa",
        "lt": "africa",
        "ly": "africa",
        "ma": "africa",
        "mi": "africa",
        "ml": "africa",
        "mo": "africa",
        "mp": "africa",
        "mr": "africa",
        "mz": "africa",
        "ng": "africa",
        "ni": "africa",
        "od": "africa",
        "pu": "africa",
        "rw": "africa",
        "se": "africa",
        "sf": "africa",
        "sg": "africa",
        "sh": "africa",
        "sl": "africa",
        "so": "africa",
        "su": "africa",
        "to": "africa",
        "tp": "africa",
        "ts": "africa",
        "tz": "africa",
        "ug": "africa",
        "uv": "africa",
        "wa": "africa",
        "wi": "africa",
        "wz": "africa",
        "za": "africa",
        "zi": "africa",
        "ay": "antarctica",
        "bv": "antarctica",
        "fs": "antarctica",
        "hm": "antarctica",
        "aq": "australia-oceania",
        "as": "australia-oceania",
        "at": "australia-oceania",
        "bp": "australia-oceania",
        "ck": "australia-oceania",
        "cq": "australia-oceania",
        "cr": "australia-oceania",
        "cw": "australia-oceania",
        "fj": "australia-oceania",
        "fm": "australia-oceania",
        "fp": "australia-oceania",
        "gq": "australia-oceania",
        "kr": "australia-oceania",
        "kt": "australia-oceania",
        "nc": "australia-oceania",
        "ne": "australia-oceania",
        "nf": "australia-oceania",
        "nh": "australia-oceania",
        "nr": "australia-oceania",
        "nz": "australia-oceania",
        "pc": "australia-oceania",
        "ps": "australia-oceania",
        "rm": "australia-oceania",
        "tl": "australia-oceania",
        "tn": "australia-oceania",
        "tv": "australia-oceania",
        "um": "australia-oceania",
        "wf": "australia-oceania",
        "wq": "australia-oceania",
        "ws": "australia-oceania",
        "aa": "central-america-n-caribbean",
        "ac": "central-america-n-caribbean",
        "av": "central-america-n-caribbean",
        "bb": "central-america-n-caribbean",
        "bf": "central-america-n-caribbean",
        "bh": "central-america-n-caribbean",
        "bq": "central-america-n-caribbean",
        "cj": "central-america-n-caribbean",
        "cs": "central-america-n-caribbean",
        "cu": "central-america-n-caribbean",
        "do": "central-america-n-caribbean",
        "dr": "central-america-n-caribbean",
        "es": "central-america-n-caribbean",
        "gj": "central-america-n-caribbean",
        "gt": "central-america-n-caribbean",
        "ha": "central-america-n-caribbean",
        "ho": "central-america-n-caribbean",
        "jm": "central-america-n-caribbean",
        "mh": "central-america-n-caribbean",
        "nn": "central-america-n-caribbean",
        "nu": "central-america-n-caribbean",
        "pm": "central-america-n-caribbean",
        "rn": "central-america-n-caribbean",
        "rq": "central-america-n-caribbean",
        "sc": "central-america-n-caribbean",
        "st": "central-america-n-caribbean",
        "tb": "central-america-n-caribbean",
        "td": "central-america-n-caribbean",
        "tk": "central-america-n-caribbean",
        "uc": "central-america-n-caribbean",
        "vc": "central-america-n-caribbean",
        "vi": "central-america-n-caribbean",
        "vq": "central-america-n-caribbean",
        "kg": "central-asia",
        "kz": "central-asia",
        "rs": "central-asia",
        "ti": "central-asia",
        "tx": "central-asia",
        "uz": "central-asia",
        "bm": "east-n-southeast-asia",
        "bx": "east-n-southeast-asia",
        "cb": "east-n-southeast-asia",
        "ch": "east-n-southeast-asia",
        "hk": "east-n-southeast-asia",
        "id": "east-n-southeast-asia",
        "ja": "east-n-southeast-asia",
        "kn": "east-n-southeast-asia",
        "ks": "east-n-southeast-asia",
        "la": "east-n-southeast-asia",
        "mc": "east-n-southeast-asia",
        "mg": "east-n-southeast-asia",
        "my": "east-n-southeast-asia",
        "pf": "east-n-southeast-asia",
        "pg": "east-n-southeast-asia",
        "pp": "east-n-southeast-asia",
        "rp": "east-n-southeast-asia",
        "sn": "east-n-southeast-asia",
        "th": "east-n-southeast-asia",
        "tt": "east-n-southeast-asia",
        "tw": "east-n-southeast-asia",
        "vm": "east-n-southeast-asia",
        "al": "europe",
        "an": "europe",
        "au": "europe",
        "ax": "europe",
        "be": "europe",
        "bk": "europe",
        "bo": "europe",
        "bu": "europe",
        "cy": "europe",
        "da": "europe",
        "dx": "europe",
        "ei": "europe",
        "en": "europe",
        "ez": "europe",
        "fi": "europe",
        "fo": "europe",
        "fr": "europe",
        "gi": "europe",
        "gk": "europe",
        "gm": "europe",
        "gr": "europe",
        "hr": "europe",
        "hu": "europe",
        "ic": "europe",
        "im": "europe",
        "it": "europe",
        "je": "europe",
        "jn": "europe",
        "kv": "europe",
        "lg": "europe",
        "lh": "europe",
        "lo": "europe",
        "ls": "europe",
        "lu": "europe",
        "md": "europe",
        "mj": "europe",
        "mk": "europe",
        "mn": "europe",
        "mt": "europe",
        "nl": "europe",
        "no": "europe",
        "pl": "europe",
        "po": "europe",
        "ri": "europe",
        "ro": "europe",
        "si": "europe",
        "sm": "europe",
        "sp": "europe",
        "sv": "europe",
        "sw": "europe",
        "sz": "europe",
        "uk": "europe",
        "up": "europe",
        "vt": "europe",
        "ae": "middle-east",
        "aj": "middle-east",
        "am": "middle-east",
        "ba": "middle-east",
        "gg": "middle-east",
        "gz": "middle-east",
        "ir": "middle-east",
        "is": "middle-east",
        "iz": "middle-east",
        "jo": "middle-east",
        "ku": "middle-east",
        "le": "middle-east",
        "mu": "middle-east",
        "qa": "middle-east",
        "sa": "middle-east",
        "sy": "middle-east",
        "tu": "middle-east",
        "we": "middle-east",
        "ym": "middle-east",
        "bd": "north-america",
        "ca": "north-america",
        "gl": "north-america",
        "ip": "north-america",
        "mx": "north-america",
        "sb": "north-america",
        "us": "north-america",
        "ar": "south-america",
        "bl": "south-america",
        "br": "south-america",
        "ci": "south-america",
        "co": "south-america",
        "ec": "south-america",
        "fk": "south-america",
        "gy": "south-america",
        "ns": "south-america",
        "pa": "south-america",
        "pe": "south-america",
        "sx": "south-america",
        "uy": "south-america",
        "ve": "south-america",
        "af": "south-asia",
        "bg": "south-asia",
        "bt": "south-asia",
        "ce": "south-asia",
        "in": "south-asia",
        "io": "south-asia",
        "mv": "south-asia",
        "np": "south-asia",
        "pk": "south-asia"
    }

    iso3_to_income = {
        "ABW": "HIC",
        "AFG": "LIC",
        "AGO": "LMC",
        "ALB": "UMC",
        "AND": "HIC",
        "ARE": "HIC",
        "ARG": "UMC",
        "ARM": "UMC",
        "ASM": "HIC",
        "ATG": "HIC",
        "AUS": "HIC",
        "AUT": "HIC",
        "AZE": "UMC",
        "BDI": "LIC",
        "BEL": "HIC",
        "BEN": "LMC",
        "BFA": "LIC",
        "BGD": "LMC",
        "BGR": "UMC",
        "BHR": "HIC",
        "BHS": "HIC",
        "BIH": "UMC",
        "BLR": "UMC",
        "BLZ": "UMC",
        "BMU": "HIC",
        "BOL": "LMC",
        "BRA": "UMC",
        "BRB": "HIC",
        "BRN": "HIC",
        "BTN": "LMC",
        "BWA": "UMC",
        "CAF": "LIC",
        "CAN": "HIC",
        "CHE": "HIC",
        "CHI": "HIC",
        "CHL": "HIC",
        "CHN": "UMC",
        "CIV": "LMC",
        "CMR": "LMC",
        "COD": "LIC",
        "COG": "LMC",
        "COL": "UMC",
        "COM": "LMC",
        "CPV": "LMC",
        "CRI": "UMC",
        "CUB": "UMC",
        "CUW": "HIC",
        "CYM": "HIC",
        "CYP": "HIC",
        "CZE": "HIC",
        "DEU": "HIC",
        "DJI": "LMC",
        "DMA": "UMC",
        "DNK": "HIC",
        "DOM": "UMC",
        "DZA": "LMC",
        "ECU": "UMC",
        "EGY": "LMC",
        "ERI": "LIC",
        "ESP": "HIC",
        "EST": "HIC",
        "ETH": "LIC",
        "FIN": "HIC",
        "FJI": "UMC",
        "FRA": "HIC",
        "FRO": "HIC",
        "FSM": "LMC",
        "GAB": "UMC",
        "GBR": "HIC",
        "GEO": "UMC",
        "GHA": "LMC",
        "GIB": "HIC",
        "GIN": "LMC",
        "GMB": "LIC",
        "GNB": "LIC",
        "GNQ": "UMC",
        "GRC": "HIC",
        "GRD": "UMC",
        "GRL": "HIC",
        "GTM": "UMC",
        "GUM": "HIC",
        "GUY": "HIC",
        "HKG": "HIC",
        "HND": "LMC",
        "HRV": "HIC",
        "HTI": "LMC",
        "HUN": "HIC",
        "IDN": "UMC",
        "IMN": "HIC",
        "IND": "LMC",
        "IRL": "HIC",
        "IRN": "LMC",
        "IRQ": "UMC",
        "ISL": "HIC",
        "ISR": "HIC",
        "ITA": "HIC",
        "JAM": "UMC",
        "JOR": "LMC",
        "JPN": "HIC",
        "KAZ": "UMC",
        "KEN": "LMC",
        "KGZ": "LMC",
        "KHM": "LMC",
        "KIR": "LMC",
        "KNA": "HIC",
        "KOR": "HIC",
        "KWT": "HIC",
        "LAO": "LMC",
        "LBN": "LMC",
        "LBR": "LIC",
        "LBY": "UMC",
        "LCA": "UMC",
        "LIE": "HIC",
        "LKA": "LMC",
        "LSO": "LMC",
        "LTU": "HIC",
        "LUX": "HIC",
        "LVA": "HIC",
        "MAC": "HIC",
        "MAF": "HIC",
        "MAR": "LMC",
        "MCO": "HIC",
        "MDA": "UMC",
        "MDG": "LIC",
        "MDV": "UMC",
        "MEX": "UMC",
        "MHL": "UMC",
        "MKD": "UMC",
        "MLI": "LIC",
        "MLT": "HIC",
        "MMR": "LMC",
        "MNE": "UMC",
        "MNG": "LMC",
        "MNP": "HIC",
        "MOZ": "LIC",
        "MRT": "LMC",
        "MUS": "UMC",
        "MWI": "LIC",
        "MYS": "UMC",
        "NAM": "UMC",
        "NCL": "HIC",
        "NER": "LIC",
        "NGA": "LMC",
        "NIC": "LMC",
        "NLD": "HIC",
        "NOR": "HIC",
        "NPL": "LMC",
        "NRU": "HIC",
        "NZL": "HIC",
        "OMN": "HIC",
        "PAK": "LMC",
        "PAN": "HIC",
        "PER": "UMC",
        "PHL": "LMC",
        "PLW": "UMC",
        "PNG": "LMC",
        "POL": "HIC",
        "PRI": "HIC",
        "PRK": "LIC",
        "PRT": "HIC",
        "PRY": "UMC",
        "PSE": "UMC",
        "PYF": "HIC",
        "QAT": "HIC",
        "ROU": "HIC",
        "RUS": "UMC",
        "RWA": "LIC",
        "SAU": "HIC",
        "SDN": "LIC",
        "SEN": "LMC",
        "SGP": "HIC",
        "SLB": "LMC",
        "SLE": "LIC",
        "SLV": "UMC",
        "SMR": "HIC",
        "SOM": "LIC",
        "SRB": "UMC",
        "SSD": "LIC",
        "STP": "LMC",
        "SUR": "UMC",
        "SVK": "HIC",
        "SVN": "HIC",
        "SWE": "HIC",
        "SWZ": "LMC",
        "SXM": "HIC",
        "SYC": "HIC",
        "SYR": "LIC",
        "TCA": "HIC",
        "TCD": "LIC",
        "TGO": "LIC",
        "THA": "UMC",
        "TJK": "LMC",
        "TKM": "UMC",
        "TLS": "LMC",
        "TON": "UMC",
        "TTO": "HIC",
        "TUN": "LMC",
        "TUR": "UMC",
        "TUV": "UMC",
        "TWN": "HIC",
        "TZA": "LMC",
        "UGA": "LIC",
        "UKR": "LMC",
        "URY": "HIC",
        "USA": "HIC",
        "UZB": "LMC",
        "VCT": "UMC",
        "VEN": "INX",
        "VGB": "HIC",
        "VIR": "HIC",
        "VNM": "LMC",
        "VUT": "LMC",
        "WSM": "LMC",
        "XKX": "UMC",
        "YEM": "LIC",
        "ZAF": "UMC",
        "ZMB": "LMC",
        "ZWE": "LM",
    }
