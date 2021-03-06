Wireguard Database Connector Overview
=====================================
Development Status: 0.1.7 (alpha)

First of all, I'd like to thank Jared McKnight for
[wireguard](https://github.com/fictivekin/wireguard) who inspired me to make
this AddOn.

The Wireguard Database Connector makes use of the ORM peewee,
providing a broader approach to several database systems.
Focused within this project is to store a wireguard configuration with import of configuration files.
Checks for a wireguard configuration are done using the optional, but strongly recommended, python module (see above).

Database backends tested for far:
* sqlite3
* mariadb
* postgres
* **Please report here more if successful tested and/or commit your code**

In most cases the use of cython is recommended.

*DB Field & Function policy:* Only compatible fields/functions among the DB types are used to support migrations from one to the other.

For more known python modules consult the peewee documentation:
<https://docs.peewee-orm.com/en/latest/peewee/database.html>

Quick Start using a database
----------------------------
### First run on python3 (=>3.6)
One the first create a default configfile at */etc/wireguard/wireguard.yaml*
```python3
from wireguard_db.models.config import DBConfig
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
You do not need to create the tables, *DBConnect()* will create these, if the tables do not exist.
Using *python* again, you can now try:
```python3
from wireguard_db.models import DBConfig, DBConnect, WGData, WGRelation
# try a connection
# in short for the default sqlite3 adapter
db = DBConnect(DBConfig.read()).get()
server = WGData()
relation = WGRelation()
# try a different database, if this is your db.
setup = DBConfig().read(config_adapter='mysql')
db_mysql = DBConnect(setup).get()
dbData = WGData()
dbRelation = WGRelation()
# both result in a peewee DatabaseProxy() object
# which are assigned to the tables.
```
Depending on the adapter one should now find empty tables in the database.
Your setup should be completed at this step.
#### Create a simple server row
```python3
dbData = WGData()
dbData.description = 'test-wg33'
# REVIEW: ATOW wireguard model isn't capable
# to add more than one IP to one interface
dbData.wg_address = '192.168.0.1/24'
if 1 == dbData.save():
    print('Could not add the row')
# check within your DB that a table row exists
```
It's time to create a real server config from this row.
```python3
from wireguard_db.utils import dicts
# the row is still active, retrieve a dict
row = dbData.get_dict()
# translate db row to parameters
wireguard_params = wgdata2wireguard(row)
print(wireguard_params)

from wireguard.server import Server
subnet = wireguard_params.pop('address')
server = Server(dbData.description, subnet, **wireguard_params)
```
### Further reading
[comment]: <> ([Tutorial](docs/Tutorial.md)
* [wireguardDB installation](docs/README-DB.md)
* [peewee documentation](http://docs.peewee-orm.com/en/latest/)
* python module [wireguard](https://github.com/fictivekin/wireguard/blob/master/README.rst)
