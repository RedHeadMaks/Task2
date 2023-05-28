def sortedDict(dict1):
    sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict