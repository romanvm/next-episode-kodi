# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import sys
if sys.version_info[1] >= 7:
    import json
else:
    import simplejson as json
import xbmc


def json_request(method, params):
    """
    Send JSON-RPC to Kodi

    :param method: Kodi JSON-RPC method
    :type method: str
    :param params: method parameters
    :type params: dict
    :return: JSON-RPC response
    :rtype: dict
    """
    return json.loads(xbmc.executeJSONRPC(json.dumps({
        'jsonrpc': '2.0', 'method': method, 'params': params, 'id': '1'
    })))
