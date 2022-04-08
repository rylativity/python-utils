from collections import abc
from typing import Any, Callable, Dict, List, Optional, Union


def remove_nulls(data: Union[List, Dict],
                 value_filter: Optional[Callable[[Any], bool]] = None) -> Union[List, Dict]:
    """ Given a list or dict, returns an object of the same structure without filtered values.

    By default, key-value pairs where the value is 'None' are removed. The `value_filter` param
    must be a function which takes values from the provided dict/list structure, and returns a
    truthy value if the key-value pair is to be removed, and a falsey value otherwise.

    Args:
        data (Union[List, Dict]): List or dict containing data
        value_filter (Optional[Callable[[Any], bool]], optional): Lambda function to use to filter out values (e.g. "lambda x: x in (None, 'NULL', 'null')"). Defaults to None.

    Raises:
        TypeError: Raise TypeError if an unsupported data type is encountered

    Returns:
        Union[List, Dict]: Returns a filtered version of the list or dictionary passed to the function call

    Taken and modified from https://stackoverflow.com/questions/67806380/recursive-remove-all-keys-that-have-null-as-value
    """
    collection_types = (list, tuple) # avoid including 'str' here
    mapping_types = (abc.Mapping,)
    all_supported_types = (*mapping_types, *collection_types)
    if value_filter is None:
        value_filter = lambda x: x is None
    if isinstance(data, collection_types):
        data = [d for d in data if not value_filter(d)] # Remove Nones at root level of list
        return [remove_nulls(x, value_filter) if isinstance(x, all_supported_types) else x for x in data]
    elif isinstance(data, mapping_types):
        clean_val = lambda x: remove_nulls(x, value_filter) if isinstance(x, all_supported_types) else x
        return {k: clean_val(v) for k, v in data.items() if not value_filter(v)}
    raise TypeError(f"Unsupported type '{type(data)}': {data!r}")

# data = {
#     "field_1":None,
#     "field_2":"b",
#     "field_3":{"z":"z","y":"y","x":None},
#     "field_4":[{"z":"z","y":"y","x":None}, None, {"z":"z","y":None, "x":{"a":None,"b":"b"}}]
# }
# print(remove_nulls(data))
