# -*- coding: utf-8 -*-
__version__ = "0.1.5"
__license__ = "GPLv3"
__docformat__ = "reStructuredText"

import sys
from peewee import DatabaseProxy, SqliteDatabase, MySQLDatabase, PostgresqlDatabase
from .constants import HAS_SQLITE3, HAS_POSTGRES, HAS_MYSQL
from .tables import database, MODELS


class DBConnect:
    """
    Set up a database connection with the requested driver/adapter using peewee adapters
    """

    def __init__(self, setup: tuple = None):
        """
        Initialize a database connector on given setup
        :param config: dict: Optional, the setup from DBConfig.get(), can be setup later
        ivar _adapter: str: adapter name
        ivar _database: obj: peewee.DatabaseProxy
        ivar _connected: bool: connected state of db
        """
        self._adapter = None
        self._database = None
        self._connected = False

        if setup:
            # full init if setup is given
            self.set(setup)

    def set(self, setup: tuple):
        """
        Sets the corresponding peewee connector for the requested database
        :param setup: tuple: as returned from DBConfig.read()
        :returns: None
        """
        if not isinstance(setup, tuple) and 2 == len(setup):
            raise ValueError('"setup" invalid allowed is one tuple.')

        _adapter, adapter_param = setup
        if not (isinstance(_adapter, str) and isinstance(adapter_param, dict)):
            raise ValueError(
                '"setup" format invalid: Hint: (adapter: str,setup: dict).'
            )

        if "sqlite3" == _adapter:
            if not HAS_SQLITE3:
                raise ImportError('driver missing: Hint "pip3 install PyMySQL"')

            adapter = SqliteDatabase(
                adapter_param["database"], pragmas=adapter_param["connect"]
            )

        elif "mysql" == _adapter:
            if not HAS_MYSQL:
                raise ImportError('driver missing: Hint "pip3 install PyMySQL"')

            adapter = MySQLDatabase(
                adapter_param["database"], **adapter_param["connect"]
            )

        elif "postgresql" == _adapter:
            if not HAS_POSTGRES:
                raise ImportError('driver missing: Hint "pip3 install psycopg2"')

            adapter = PostgresqlDatabase(
                adapter_param["database"], **adapter_param["connect"]
            )
        else:
            raise ValueError(f'"{_adapter}" not implemented.')

        database.initialize(adapter)
        self._adapter = _adapter

        database.bind(MODELS)
        self._database = database
        self.check()

    def get(self):
        """
        Get the connected database proxy object
        :returns: peewee.DatabaseProxy (injected into tables)
        :rtype: object
        """
        try:
            self._database.connect(reuse_if_open=True)
            self._connected = True
        except Exception as connect_error:
            self._connected = False
            print(f'Connect using adapter "{self._adapter}" failed', file=sys.stderr)
            raise connect_error

        return self._database

    @property
    def connected(self):
        """
        Return connection state
        :returns: True if connected
        :rtype: bool
        """
        return self._connected

    @property
    def adapter(self):
        """
        Returns the used adapter
        :returns: adapter name as in config
        :rtype: str
        """
        return self._adapter

    def check(self):
        """
        Sanitizer: checks and creates tables, if they do not exist
        :returns: None
        """
        for table in MODELS:
            table.validate_model()
            table.create_table(safe=True)
        self._connected = True

    def close(self):
        """
        Close the database and set connected to False
        :returns: None
        """
        self._database.close()
        self._connected = False

    def __repr__(self):
        """
        Show use adapter and connected state
        :returns: a text line
        :rtype: str
        """
        return str(
            f'DBConnect: Adapter "{self._adapter}", connected "{self._connected}"'
        )
