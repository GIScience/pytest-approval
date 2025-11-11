def sort_dict(dictionary: dict) -> dict:
    result = {}
    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            result[k] = sort_dict(v)
        else:
            result[k] = v
    return result
