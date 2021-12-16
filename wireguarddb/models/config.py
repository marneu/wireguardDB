# -*- coding: utf-8 -*-
__version__ = "0.1.7"
__license__ = "GPLv3"
__docformat__ = "reStructuredText"

import os
from pathlib import Path
import yaml
from .constants import (  # pylint: disable=relative-beyond-top-level
    ADAPTERS,
    CONFIG_PATH,
    DBCONFIG_FILE,
    SAMPLE_CONFIG,
)


class DBConfig:
    """
    Read/write a config file for the wireguard DB connector
    """

    def __init__(self):
        """
        ivar _configfile: pathlib.Path: db config file
        ivar _adapter: str: DB adapter
        ivar _setup: tuple: setup for DBConnect
        """
        self._configfile = None
        self._adapter = None
        self._setup = None

    @property
    def filename(self):
        """
        Gets (and sets) the config filename for use with read/write.
        :returns: full path db config filename
        :rtype: str
        """
        if self._configfile is None:
            return None

        return self._configfile.resolve()

    @filename.setter
    def filename(self, full_path_filename: str):
        """
        Sets the filename
        :param full_path_filename: str: filename including path
        """
        if not isinstance(full_path_filename, str):
            raise ValueError(f'"{full_path_filename}" is not a string')

        if any(char in full_path_filename for char in ("*", "?")):
            raise ValueError(f'globs not allowed in "{full_path_filename}"')

        if os.path.sep not in full_path_filename:
            configfile = Path(CONFIG_PATH, full_path_filename)
        else:
            configfile = Path(full_path_filename)

        if configfile.is_dir():
            raise ValueError(f'"{configfile.name}" is a directory')

        self._configfile = configfile

    def read(
        self, *, config_adapter: str = "defaults", config_file: str = "default"
    ):  # pylint: disable=too-many-branches
        """
        Reads a config file
        :param config_adapter: str, optional: any of
                ('defaults', 'sqlite3', 'mysql', 'postgresql')
                ('defaults' reads the default adapter from config file)
        :param config_file: str, optional: filename inclusive path to be used
                ('default' uses previous set filename)
        :returns: (adapter: str, setup: dict)
        :rtype: tuple
        """
        # initialize class vars
        self._adapter = ""
        self._setup = None

        if not isinstance(config_adapter, str):
            raise ValueError('Parameter "config_adapter" is not a string')

        if not isinstance(config_file, str):
            raise ValueError('Parameter "config_file" is not a string')

        if "default" == config_file and self._configfile is None:
            self.filename = CONFIG_PATH + os.path.sep + DBCONFIG_FILE

        elif "default" != config_file:
            self.filename = config_file

        if self._configfile is None:
            raise ValueError("No filename provided.")

        configfile = self._configfile

        if not configfile.is_file():
            raise ValueError(f'"{configfile}" does not exist.')

        with configfile.open("r", encoding="utf8") as config:
            setup = yaml.safe_load(config)

        adapter = None

        if "defaults" == config_adapter:

            if 1 == len(setup):
                # old style, only one db block
                adapter = next(iter(setup))

            elif "defaults" in setup and "adapter" in setup["defaults"]:
                adapter = setup["defaults"]["adapter"]

        else:
            adapter = config_adapter

        if adapter is None:
            raise ValueError(f'Adapter "{config_adapter}" not configured.')

        if adapter not in ADAPTERS:
            raise ValueError(f'"{adapter}" not implemented')

        if adapter not in setup:
            raise LookupError(
                f'Missing adapter section "{adapter}" in config "{configfile}"'
            )

        if "database" not in setup[adapter]:
            raise LookupError(
                f'Missing "database" key for "{adapter}" in config "{configfile}"'
            )

        if "connect" not in setup[adapter]:
            print(f'WARN: Missing "connect" section for "{adapter}", using defaults.')
            setup[adapter]["connect"] = {}

        self._configfile = configfile
        self._adapter = adapter
        self._setup = (self._adapter, setup[adapter])

        return self._setup

    @property
    def getadapter(self):
        """
        Get adapter name
        :returns: adapter name
        :rtype: str
        """
        return self._adapter

    @property
    def getsetup(self):
        """
        Get setup
        :returns: setup for adapter
        :rtype: tuple
        """
        return self._setup

    def write(self, *, overwrite: bool = False):
        """
        Writes the configfile:
          If a read() was issued before, a plain setup block for this adapter will be written.
          If issued without prior .read(), a default config will be written.
          If a config filename has not been provided before, CONFIG_PATH/DBCONFIG_FILE is used.
        param overwrite: bool: Overwrite file if exists
                (default = False)
        :returns: True if written
        :rtype: bool
        """
        if self._configfile is None:
            self._configfile = Path(CONFIG_PATH, DBCONFIG_FILE).resolve()

        if not overwrite and self._configfile.is_file():
            raise FileExistsError(
                f'"{self._configfile}" exists and overwrite = {overwrite}'
            )

        if bool(self._setup):
            config = {
                "defaults": {"adapter": self._adapter},
                self._adapter: self._setup,
            }
        else:
            config = SAMPLE_CONFIG

        with self._configfile.open("w", encoding="utf8") as configfile:
            if isinstance(config, dict):
                yaml.dump(
                    config, configfile, default_flow_style=False, allow_unicode=True
                )
            else:
                configfile.write(config)

        return True
