Wireguard Database Connector Overview
=====================================
Development Status: 0.1.7 (alpha)

First of all, I'd like to thank Jared McKnight for
[wireguard](https://github.com/fictivekin/wireguard) who inspired me to make
this AddOn.

The Wireguard Database Connector makes use of the ORM peewee,
providing a broader approach to several database systems.

DB Field & Function policy: Only compatible fields/functions are used to support migrations from one to the other.

Database backends tested for far:
* sqlite3
* mariadb
* postgres
* **Please report here more if successful tested and/or commit your code**

In most cases the use of cython is recommended.

For more known python modules consult the peewee documentation:
<https://docs.peewee-orm.com/en/latest/peewee/database.html>

Common used DB's are (install to your needs):
* SQLite: [sqlite3](https://docs.python.org/3.8/library/sqlite3.html) (mostly included in modern python versions)
* MySQL (MariaDB): [pymysql](https://pypi.org/project/PyMySQL/)
* Postgres: [psycopg2](https://pypi.org/project/psycopg2/)

```bash
# common
python3 -m pip install cython
# example for MySQL/MariaDB usage
python3 -m pip install PyMySQL
# example for Postgres (may not succeed -> read docs/README-DB2.md)
python3 -m pip install psycopg2
# common
python3 -m pip install peewee
```

Quick Start using Database
--------------------------
### First run python3
One the first run we will create a default configfile at */etc/wireguard/wireguard.yaml*
```python3
from wireguarddb.models import DBConfig
# now enshure you can write and read the config.yaml
# it will create a /etc/wireguard/wireguard.yaml file
if DBConfig().write():
    setup = DBConfig().read()
setup
# you should see a tuple containing the default setup for a sqlite3 connector
exit()
```
You just have created a sample configfile and should edit this
to your needs. Errors may indicate that you are either not authorized
to use or create files in */etc/wirguard* or the directory itself does not exist.
If you are using one database type (*adapter*) only you do not need to remove
any other of the sections for other adpters.

The default */etc/wireguard/wireguard.yaml* should be self
explaining for those used in working with databases on a system level.

#### SQLite3
If using a Linux standard directory structure, you may consider creating the directory
*/var/lib/wireguard/*. And set the *database* to this directory.
The *connect* Parameters specify the *pragmas*.

#### MySQL, PostgreSQL etc.
You need to create the database and access rights, the tables will be created automatically.
```sql
/* MariaDB Example - ATT: Use your own names here! */
CREATE DATABASE wgdb;
CREATE USER wguser@localhost IDENTIFIED BY 'yourpassword';
GRANT ALL privileges ON wgdb.* TO wguser@localhost;
FLUSH PRIVILEGES;
```
If this is your default database, the corresponding */etc/wireguard/wireguard.yaml* section should look like (changes only):
```yaml
defaults:
    adapter: mysql
mysql:
    database: wgdb
    connect:
        user: wguser
        password: yourpassword
```
If *mysql* is not set within '*defaults*' section,
you have to pass the parameter to *DBconfig().read()*:
```python3
from wireguarddb.models import DBConfig
# set config
setup = DBConfig().read('mysql')
# set dbconfig and connect
setup
exit()
```
### Further reading
* [Usage examples](docs/README-DB2.md)
* [peewee documentation](http://docs.peewee-orm.com/en/latest/)
* [wireguard module](https://github.com/fictivekin/wireguard/blob/master/README.rst)
