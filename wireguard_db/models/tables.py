# -*- coding: utf-8 -*-
__version__ = "0.1.8"
__license__ = "GPLv3"
__docformat__ = "reStructuredText"

from datetime import datetime
from peewee import (
    DatabaseProxy,
    Model,
    CharField,
    IntegerField,
    BooleanField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)


class UnknownField(object):  # pylint: disable=too-few-public-methods
    """
    Unknown Field - placeholder
    """

    def __init__(self, *_, **__):
        pass


# passed as placeholder to the tables
database = DatabaseProxy()


class BaseModel(Model):  # pylint: disable=too-few-public-methods
    """
    Basics used for Models
    """

    def get_dict(self):
        """
        Returns the row as dict
        :returns: active row as dict
        :rtype: dict
        """
        return self.__dict__["__data__"]

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Pull in basics from Model like id field, database
        Sets save only changed fields
        """

        database = database
        only_save_dirty = True


class WGData(BaseModel):
    """
    wireguard config data derived from peewee.Model
    Fieldnames beginning with 'wg_' are used for configuration
    :field config_class: class used to construct the configuration
    """
    # wireguard model required
    config_class = CharField(max_length=24, null=True)
    description = CharField(max_length=80)
    # only wg_ fields are used within a config file
    wg_interface = CharField(max_length=8, null=True, index=True)
    wg_address = CharField(index=True)
    wg_saveconfig = BooleanField(null=True)
    wg_dns = CharField(null=True)
    wg_publickey = CharField(max_length=48, null=True)
    wg_privatekey = CharField(max_length=48, null=True, unique=True)
    wg_presharedkey = CharField(max_length=48, null=True)
    wg_endpoint = CharField(null=True, index=True)
    wg_listenport = IntegerField(null=True)
    wg_allowedips = CharField(null=True)
    wg_persistentkeepalive = IntegerField(null=True)
    wg_preup = TextField(null=True)
    wg_postup = TextField(null=True)
    wg_predown = TextField(null=True)
    wg_postdown = TextField(null=True)
    wg_table = CharField(max_length=10, null=True)
    wg_mtu = IntegerField(null=True)
    # service part
    is_enabled = BooleanField(default=True)
    is_connected = BooleanField(default=False)
    # revision part
    is_readonly = BooleanField(default=False)
    updated = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    created = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # other ref: ref to a host table if you use this
    host_id = IntegerField(index=True, null=True)

    def save(self, force_insert: bool = False, only: list = None):
        """
        Simulates an on_updated timestamp, and takes care of insert/update behaviour
        :param force_insert: bool: Force INSERT query
        :param only: list/tuple: optional list of fields to be updated/inserted.
        :returns: Number of rows modified.
        :rtype: int
        """

        # if this row is new (id=None), default will apply
        if not force_insert:
            self.updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return super().save(force_insert=force_insert, only=only)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        mostly derived from BaseModel
        """
        table_name = "WGData"


class WGRelation(BaseModel):
    """
    Relation between server/peers or peer to peer (1-1)
    """
    WGParent = ForeignKeyField(WGData, backref="Parent")
    WGPeer = ForeignKeyField(WGData, backref="Peer")
    created = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        mostly derived from BaseModel
        """
        table_name = "WGRelation"
        indexes = ((("WGParent", "WGPeer"), True),)


MODELS = (WGData, WGRelation)
