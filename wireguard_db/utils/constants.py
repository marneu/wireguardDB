# -*- coding: utf-8 -*-
__version__ = "0.1.3"
__license__ = "GPLv3"
__docformat__ = "reStructuredText"

DB_WIREGUARD_PARAMS_MAP = {
    # DB field : wireguard parameter
    "wg_listenport": "port",
    "wg_privatekey": "private_key",
    "wg_publickey": "public_key",
    "wg_presharedkey": "preshared_key",
    "wg_allowedips": "allowed_ips",
    "wg_saveconfig": "save_config",
    "wg_postup": "post_up",
    "wg_preup": "pre_up",
    "wg_postdown": "post_down",
    "wg_predown": "pre_down",
    "wg_persistentkeepalive": "keepalive",
}
