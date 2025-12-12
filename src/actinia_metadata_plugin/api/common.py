#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Common api methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import make_response, jsonify

from actinia_metadata_plugin.model.responseModels import \
    SimpleStatusCodeResponseModel
from actinia_metadata_plugin.core import common
from actinia_metadata_plugin.resources.config import GEONETWORK
from actinia_metadata_plugin.resources.logging import log


def checkConnection(name):
    """ Method to test connection

    Args:
      name (string): resource to test. Can be 'actinia-core' or 'geonetwork'

    Returns:
      response (Response): of type SimpleStatusCodeResponseModel telling
      connection success or failure
    """

    if name == 'geonetwork':
        url = GEONETWORK.csw_url
        name = 'geonetwork'
        type = 'xml'

    try:
        records = common.checkConnection(url, name, type)
    except Exception:
        log.error("Don't know which connection to test")

    if records is not None:
        res = jsonify(SimpleStatusCodeResponseModel(
            status=200, message="success"))
        return make_response(res, 200)
    elif records is None:
        res = jsonify(SimpleStatusCodeResponseModel(
            status=404, message="failure"))
        return make_response(res, 200)


def checkConnectionWithoutResponse(name):
    """ Method to test connection

    Args:
      name (string): resource to test. Can be 'actinia-core' or 'geonetwork'
    """

    if name == 'geonetwork':
        url = GEONETWORK.csw_url
        name = 'geonetwork'
        type = 'xml'

    try:
        connectionTest = common.checkConnection(url, name, type)
        return connectionTest
    except Exception:
        log.error("Don't know which connection to test")
        return None
