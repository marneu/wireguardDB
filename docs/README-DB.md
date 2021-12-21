# Installation instructions

## Preseedings
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
### Database adapters
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
from wireguard_db.models.config import DBConfig
# set config
setup = DBConfig().read(config_adapter='mysql')
# set dbconfig and connect
setup
exit()
```
## Extending tables
**NOTE:** I don't recommend expanding base tables.
Better to create your own table and set a foreign key for the id field
to add what you need to your table.
If you insist on adding fields, don't start the field name with an uppercase letter,
these are used for configuration and can be disruptive.

## Ubuntu 20.04 Findings
### PostgreSQL
To use *psycopg2* you should have postgresql installed:
```bash
apt install postgresql
```
If you trust your local computer and users:
* Change within: /etc/postgresql/12/main/pg_hba.conf
```config
# Database administrative login by Unix domain socket
local   all             postgres                                trust
```
* Run as postgres user:
```bash
sudo -iu postgres
```
```bash
createuser wgdb with encrypted password '***'
psql
```
```sql
create database wgdb;
grant all privileges on database wgdb to wgdb;
```
* Install the required python module for postgresql within your project:
```bash
apt install python3-dev libpq-dev
pip3 install psycopg2
```
