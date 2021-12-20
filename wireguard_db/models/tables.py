# -*- coding: utf-8 -*-

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
    @classmethod
    def get_dict(cls, expr):
        """
        return a record as dict
        :param expr: any valid expression for select()
        :returns: Record as dict
        :rtype: dict
        """
        return cls.select().where(expr).dicts().get()

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
    Fieldnames beginning with an uppercase letter are used for configuration
    """
    description = CharField(max_length=80)
    Interface = CharField(max_length=8, null=True, index=True)
    Address = CharField(index=True)
    SaveConfig = BooleanField(null=True)
    DNS = CharField(max_length=64, null=True)
    PublicKey = CharField(max_length=48, null=True, unique=True)
    PrivateKey = CharField(max_length=48, null=True, unique=True)
    PresharedKey = CharField(max_length=48, null=True)
    Endpoint = CharField(null=True, index=True)
    ListenPort = IntegerField(null=True)
    AllowedIPs = CharField(null=True)
    PersistentKeepalive = IntegerField(null=True)
    PreUp = TextField(null=True)
    PreDown = TextField(null=True)
    PostUp = TextField(null=True)
    PostDown = TextField(null=True)
    Table = CharField(max_length=10, null=True)
    MTU = IntegerField(null=True)
    host = CharField(max_length=64, index=True, default="localhost")
    notes = TextField(null=True)
    is_connected = BooleanField(default=False)
    read_only = BooleanField(default=False)
    enabled = BooleanField(default=True)
    updated = DateTimeField(default=datetime.now)
    created = DateTimeField(default=datetime.now)

    def save(self, *,
             force_insert: bool = False,
             only: list = None,
             updated: bool = False):  # pylint: disable=arguments-differ
        """
        simulate an on_updated timestamp, and increment the counter
        :param force_insert: bool: if False update is used
        :param only: list: list of fields to update/insert
        :param updated: bool: set updated time stamp
        :returns: table
        :rtype: object
        """
        if not force_insert:
            self.updated = datetime.now()
        return super().save(force_insert=force_insert, only=only)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        mostly derived from BaseModel
        """
        table_name = "WGData"


class WGRelation(BaseModel):
    """
    relation between server/peers or peer to peer (1-1), derived from peewee.Model
    """
    wireguardServer = ForeignKeyField(WGData, backref="Server")
    wireguardPeer = ForeignKeyField(WGData, backref="PeerPartner")
    created = DateTimeField(default=datetime.now)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        mostly derived from BaseModel
        """
        table_name = "WGRelation"
        indexes = ((("wireguardServer", "wireguardPeer"), True),)


MODELS = (WGData, WGRelation)
