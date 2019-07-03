def is_query_param_set(request, name):
    return name in request.query_params


def get_query_param_str(request, name, missing_default=None):
    return request.query_params.get(name, missing_default)


def get_query_param_bool(request, name, missing_default=None, empty_default=True):
    str_value = get_query_param_str(request, name, None)
    if str_value is None:
        return missing_default
    if str_value == "":
        return empty_default
    str_value_lower = str_value.lower()
    if str_value_lower == "true" or str_value_lower == "yes" or str_value_lower == "1":
        return True
    if str_value_lower == "false" or str_value_lower == "no" or str_value_lower == "0":
        return False
    return missing_default


def get_query_param_int(request, name, missing_default=None, empty_default=None):
    str_value = get_query_param_str(request, name, None)
    if str_value is None:
        return missing_default
    if str_value == "":
        return empty_default
    try:
        return int(str_value)
    except ValueError:
        return missing_default


def get_query_param_list(request, name, missing_default=None, empty_default=[], remove_empty=True):
    str_value = get_query_param_str(request, name, None)
    if str_value is None:
        return missing_default
    if str_value == "":
        # Don't return reference to mutable default arg def
        if empty_default == []:
            return []
        return empty_default
    parts = str_value.split(",")
    if remove_empty:
        parts = list(filter(lambda part: part != "", parts))
    return parts
