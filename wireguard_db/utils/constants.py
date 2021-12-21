# -*- coding: utf-8 -*-

DB_WIREGUARD_PARAMS_MAP = {
    # DB field : wireguard parameter
    "ListenPort": "port",
    "PrivateKey": "private_key",
    "PublicKey": "public_key",
    "PresharedKey": "preshared_key",
    "AllowedIps": "allowed_ips",
    "SaveConfig": "save_config",
    "PostUp": "post_up",
    "PreUp": "pre_up",
    "PostDown": "post_down",
    "PreDown": "pre_down",
    "PersistentKeepalive": "keepalive",
}
