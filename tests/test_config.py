from pathlib import Path
import pytest
from wireguardDB.models.config import DBConfig
from wireguardDB.models.constants import CONFIG_PATH, DBCONFIG_FILE


def test_write_db_config():

    # write a default config
    test_path = Path(CONFIG_PATH, DBCONFIG_FILE)

    # short: DBConfig().write()
    config = DBConfig()
    config.write(overwrite=True)

    assert test_path.read_text()[0:9] == "defaults:"


def test_basic_db_config():

    adapter = "sqlite3"
    config = DBConfig()
    config.filename = "/etc/wireguard/wireguard.yaml"

    setup = DBConfig().read()

    assert f"{adapter}" in setup[0]


def test_adapter_is_valid():

    with pytest.raises(ValueError, match=r'"nothing" not implemented'):

        config = DBConfig()

        adapter = "nothing"
        config.filename = "/etc/wireguard/wireguard.yaml"

        config.read(config_adapter=adapter)


def test_file_not_exists():

    with pytest.raises(ValueError, match=r'"/tmp/test123config.yaml" does not exist'):

        filename = "/tmp/test123config.yaml"
        config = DBConfig()
        config.read(config_file=filename)


def test_filename_has_no_globs():

    with pytest.raises(ValueError, match=r"globs not allowed in .*"):

        config = DBConfig()
        filename = "/tmp/test*config?.yaml"
        config.filename = filename


def test_mysql_db_config():

    adapter = "mysql"

    setup = DBConfig().read()

    assert f"{adapter}" not in setup[0]
