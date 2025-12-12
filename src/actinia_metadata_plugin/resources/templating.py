#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Template loader file
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from jinja2 import Environment, PackageLoader

# this environment is used for all cases where individual templates are loaded
tplEnv = Environment(
    loader=PackageLoader('actinia_metadata_plugin', 'templates')
)
