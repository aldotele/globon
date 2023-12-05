from util.exception.filter_exception import FilterException


def build_application_filter(composite_filter: str, fields: list) -> dict:
    filter_dict = {}
    for filter in composite_filter.split("&"):
        filter = filter.strip().lower()
        if "=" in filter:
            field, value = extract_field_value(filter, "=")
            validate_field(field, fields)
            field_iexact = field + "__iexact"
            filter_dict[field_iexact] = value
        elif ">" in filter:
            field, value = extract_field_value(filter, ">")
            validate_field(field, fields)
            field_gt = field + "__gt"
            filter_dict[field_gt] = value
        elif "<" in filter:
            field, value = extract_field_value(filter, "<")
            validate_field(field, fields)
            field_lt = field + "__lt"
            filter_dict[field_lt] = value
        elif "contains" in filter:
            field, value = extract_field_value(filter, "contains")
            validate_field(field, fields)
            field_icontains = field + "__icontains"
            filter_dict[field_icontains] = value
        else:
            raise FilterException(f'filter <{filter}> not valid')
    return filter_dict


def validate_field(field, fields):
    if field not in fields:
        raise FilterException(f'field <{field}> not valid')


def validate_composite_filter(composite_filter):
    # TODO implement validation
    return


def extract_field_value(text: str, delimiter: str) -> tuple:
    text_split = text.split(delimiter)
    return text_split[0].strip().replace(".", "__"), text_split[1].strip()
