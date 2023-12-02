def build_application_filter(composite_filter: str) -> dict:
    validate_composite_filter(composite_filter)
    filter_dict = {}
    for filter in composite_filter.split("&"):
        filter = filter.strip().lower()
        if "=" in filter:
            field_name, value = extract_field_value(filter, "=")
            field_name_iexact = field_name + "__iexact"
            filter_dict[field_name_iexact] = value
        if ">" in filter:
            field_name, value = extract_field_value(filter, ">")
            field_name_gt = field_name + "__gt"
            filter_dict[field_name_gt] = value
        if "<" in filter:
            field_name, value = extract_field_value(filter, "<")
            field_name_lt = field_name + "__lt"
            filter_dict[field_name_lt] = value
        if "contains" in filter:
            field_name, value = extract_field_value(filter, "contains")
            field_name_icontains = field_name + "__icontains"
            filter_dict[field_name_icontains] = value
        # TODO implement error handling for not valid filters
    return filter_dict


def validate_composite_filter(composite_filter):
    # TODO implement validation
    return


def extract_field_value(text: str, delimiter: str) -> tuple:
    text_split = text.split(delimiter)
    return text_split[0].strip().replace(".", "__"), text_split[1].strip()
