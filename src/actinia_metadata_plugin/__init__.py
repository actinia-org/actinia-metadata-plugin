# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Init file
"""

import importlib.metadata

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'actinia_metadata_plugin.wsgi'
    __version__ = importlib.metadata.version(dist_name)
except Exception:
    __version__ = 'unknown'
