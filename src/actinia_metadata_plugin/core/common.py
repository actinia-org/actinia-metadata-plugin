#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Module for shared methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import json

import requests
import xmltodict
from requests.auth import HTTPBasicAuth

from actinia_metadata_plugin.resources.logging import log


def auth(CONFIG):
    """ Method to create HTTPBasicAuth from config credentials
    """
    user = CONFIG.user
    password = CONFIG.password

    auth = HTTPBasicAuth(user, password)

    return auth


def checkConnection(url, name, expectedFormat):
    """ Method to test connection

    Args:
      url (string): url of resource to test.
      name (string): name of resource to test. Only used for logging
      expectedFormat (string): Format in which resource will respond. Can be
        'xml' or 'json'
    """

    # can be called by e.g.
    # checkConnection(GEONETWORK.csw_url, 'geonetwork', 'xml')

    log.debug('Testing connection to ' + url)

    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        log.error('Connection Error to ' + name)
        return None

    try:
        if expectedFormat == 'xml':
            parsedresp = xmltodict.parse(resp.content)
            records = json.dumps(parsedresp)
        elif expectedFormat == 'json':
            parsedresp = json.loads(resp.text)

        log.debug('Connection successfull to ' + name)
        return True

    except Exception:
        log.error('Connection Error to ' + name)
        return None
