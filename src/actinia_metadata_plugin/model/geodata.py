#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Model classes for geodata object
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2025 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from jsonmodels import models, fields


class GeodataMeta(models.Base):
    """Model for geodata object

    This object contains the metadata from GNOS
    """
    uuid = fields.StringField()  # string
    bbox = fields.ListField([int, float])  # bbox array
    crs = fields.StringField()  # string
    table = fields.StringField()  # string
    format = fields.StringField()  # string
