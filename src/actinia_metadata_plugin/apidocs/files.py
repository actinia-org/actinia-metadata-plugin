#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Documentation objects for GNOS api endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2025 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from actinia_metadata_plugin.model.responseModels import SimpleStatusCodeResponseModel

upload_post_docs = {
    "summary": "Upload file.",
    "description": "File can be uploaded, best used with https://bmvimetadaten.mundialis.de.",
    "tags": [
        "File Management"
    ],
    "responses": {
        "200": {
            "description": "Success or failure of connection",
            "schema": SimpleStatusCodeResponseModel
        }
    }
}
