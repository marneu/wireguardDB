# -*- coding: utf-8 -*-

from collections import OrderedDict
from .constants import DB_WIREGUARD_PARAMS_MAP


# coffee goes to: https://stackoverflow.com/questions/9876059/parsing-configure-file-with-same-section-name-in-python
class MultiDict(OrderedDict):
    """
    use dict with multiple occurrences of a key
    """

    _unique = 0  # class variable

    def __setitem__(self, key, val):
        """

        :param key:
        :param val:
        :return:
        """
        if isinstance(val, dict):
            self._unique += 1
            key += str(self._unique)
        OrderedDict.__setitem__(self, key, val)


def wgdata2wireguard(wgdata_row: dict):
    """
    Prepare a db record as kwarg dict for wireguard model
    :param wgdata_row: a DB row dict
    :returns: dictionary for kwargs
    :rtype: dict
    """
    # comprehension to filter out fields with no value
    # and field names starting in lowercase
    # translate on the fly from db to parameter names and
    # lower case db fields
    return {
        DB_WIREGUARD_PARAMS_MAP.get(key, key.lower()): val
        for key, val in wgdata_row.items()
        if val is not None and key[0].isupper()
    }
