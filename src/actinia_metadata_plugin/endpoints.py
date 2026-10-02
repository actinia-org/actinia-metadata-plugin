#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2021 mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import sys

import werkzeug
from flask import current_app, send_from_directory

from actinia_metadata_plugin.api.files import Upload
from actinia_metadata_plugin.api.metadata import (
    GnosConnection,
    RawCat,
    RawTags,
    RawUuid,
    Tags,
    Uuid,
)
from actinia_metadata_plugin.resources.logging import log


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_endpoints(flask_api):

    app = flask_api.app
    apidoc = flask_api

    package = sys._getframe().f_back.f_globals["__package__"]
    if package != "actinia_core":

        @app.route("/")
        def index():
            try:
                return current_app.send_static_file("index.html")
            except werkzeug.exceptions.NotFound:
                log.debug("No index.html found. Serving backup.")
                # when actinia-metadata-plugin is installed in single mode, the
                # swagger endpoint would be "latest/api/swagger.json". As api
                # docs exist in single mode, use this fallback for plugin mode.
                return """<h1 style='color:red'>actinia-metadata-plugin</h1>
                    <a href="api/v1/swagger.json">API docs</a>"""

        @app.route("/<path:filename>")
        def static_content(filename):
            # WARNING: all content from folder "static" will be accessible!
            return send_from_directory(app.static_folder, filename)

    apidoc.add_resource(Upload, "/files")

    apidoc.add_resource(GnosConnection, "/metadata/test/connection")

    apidoc.add_resource(RawTags, "/metadata/raw/tags/<tags>")
    apidoc.add_resource(RawCat, "/metadata/raw/categories/<category>")
    apidoc.add_resource(RawUuid, "/metadata/raw/uuids/<uuid>")
    apidoc.add_resource(Tags, "/metadata/geodata/tags/<tags>")
    apidoc.add_resource(Uuid, "/metadata/geodata/uuids/<uuid>")
