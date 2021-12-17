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

Quick Start using Database
--------------------------
### First run on python3 (=>3.6)
One the first create a default configfile at */etc/wireguard/wireguard.yaml*
```python3
from wireguardDB.models.config import DBConfig
# now enshure you can write and read the config.yaml
# it will create a /etc/wireguard/wireguard.yaml file
if DBConfig().write():
    setup = DBConfig().read()
setup
# you should see a tuple containing the default setup for a sqlite3 connector
exit()
```
This should have created a sample configfile, now edit this
to your needs. Errors may indicate that you are either not authorized
to use or create files in */etc/wireguard* or the directory itself does not exist.
If you are using only one database type (*adapter*) you do not need to remove
any other of the sections for other adpters.

The default */etc/wireguard/wireguard.yaml* should be self
explaining for those used in working with databases on a system level.
#### Test a connection to your database
```python3
from wireguardDB.models import DBConfig, DBConnect
# try a connection
# in short
db = DBConnect().set(DBConfig.read())
# is
setup = DBConfig.read()
db = DBConnect().set(setup)
```
### Further reading
* [Tutorial](docs/Tutorial.md)
* [peewee documentation](http://docs.peewee-orm.com/en/latest/)
* python module [wireguard](https://github.com/fictivekin/wireguard/blob/master/README.rst)
