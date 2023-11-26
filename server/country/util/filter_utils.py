def extract_field_value(text: str, delimiter: str) -> tuple:
    text_split = text.split(delimiter)
    return text_split[0].strip(), text_split[1].strip()
