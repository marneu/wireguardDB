# -*- coding: utf-8 -*-
__version__ = "0.1.5"
__license__ = "GPLv3"
__docformat__ = "reStructuredText"

from collections import OrderedDict
from .constants import DB_WIREGUARD_PARAMS_MAP


# idea taken from: https://stackoverflow.com/questions/9876059/parsing-configure-file-with-same-section-name-in-python
class MultiDict(OrderedDict):
    """
    Used within configparser for multiple occurrences of a key.
    Adds unique (incremented) integer to the key
    """
    _keys = {}

    def __setitem__(self, key, val):
        """
        Overwrite setitem to add an increment to the key group
        :param key: str: any
        :param val: any value
        :returns: list with unique keys
        :rtype: OrderedDict
        """
        if isinstance(val, dict):

            if key not in self._keys:
                self._keys[key] = 0

            self._keys[key] += 1
            key += str(self._keys[key])

        OrderedDict.__setitem__(self, key, val)


def wgdata2wireguard(row: dict) -> dict:
    """
    Prepare one db record for wireguard model as kwargs.
    :param row: One DB row dict
    :returns: Parameters used as kwargs or None
    :rtype: dict
    """
    # comprehension to filter out fields with no value
    # and select only field names starting in 'wg_'
    # translate on the fly from db to parameter names
    if isinstance(row, dict):

        return {
            DB_WIREGUARD_PARAMS_MAP.get(key, key[3:]): val
            for key, val in row.items()
            if val is not None and 'wg_' == key[0:3]
        }

def config2wgdata(config: dict) -> dict:
    """
    Returns a dict to be witten to database.
    :param config: dict: as found within configparser
    :returns: The fields for a row or None if input fails
    :rtype: dict
    """

    if isinstance(config, dict):

        # comprehension to get comments only
        comment = ' '.join([
            str(config.pop(key)).replace('#', '').strip()
            for key, val in config.items()
            if '#' == key[0:1]
        ])

        # comprehension to prefix fields with 'wg_'
        # and filter out empty fields
        db_fields = {
            'wg_' + key: val
            for key, val in config.items()
            if val is not None
        }

        # use comment as rows description
        db_fields['description'] = comment

        return db_fields
