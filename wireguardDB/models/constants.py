# -*- coding: utf-8 -*-
__version__ = "0.1.7"

ADAPTERS = ("sqlite3", "mysql", "postgresql")

CONFIG_PATH = "/etc/wireguard"
DBCONFIG_FILE = "wireguard.yaml"
DB_FILE = "wireguard.db"

SAMPLE_CONFIG = f"""
defaults:
    # is any of the sections below
    adapter: sqlite3

# used section names so far: sqlite3, mysql, postgresql
sqlite3:
    database: {CONFIG_PATH}/{DB_FILE}
    connect:
        # will be pragmas
        journal_mode: wal
        cache_size: 10000
        foreign_keys: 1
        reuse_if_open: True

mysql:
    database: wgdb
    connect:
        # Connection credentials + Parameters
        host: localhost
        port: 3306
        user: wgdb
        password: yoyodine
        charset: 'utf8mb4'
        use_unicode: True
        sql_mode: 'PIPES_AS_CONCAT'

postgresql:
    database: wgdb
    connect:
        # Connection credentials + Parameters
        host: localhost
        port: 5432
        user: wgdb
        password: yoyodine
""".strip()  # pylint: disable=trailing-whitespace

try:
    import sqlite3  # pylint: disable=unused-import

    HAS_SQLITE3 = True
except ImportError:
    HAS_SQLITE3 = False

try:
    import pymysql  # pylint: disable=unused-import

    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

try:
    import psycopg2  # pylint: disable=unused-import

    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

# just informational for improvement tips
try:
    import cython  # pylint: disable=unused-import

    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False
