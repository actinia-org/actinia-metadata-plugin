#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import current_app, send_from_directory
import werkzeug

from actinia_metadata_plugin.resources.logging import log

from actinia_metadata_plugin.api.files import Upload
from actinia_metadata_plugin.api.metadata import GnosConnection
from actinia_metadata_plugin.api.metadata import RawTags
from actinia_metadata_plugin.api.metadata import RawCat
from actinia_metadata_plugin.api.metadata import RawUuid
from actinia_metadata_plugin.api.metadata import Tags
from actinia_metadata_plugin.api.metadata import Uuid


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_endpoints(flask_api):

    app = flask_api.app
    apidoc = flask_api

    @app.route('/')
    def index():
        try:
            return current_app.send_static_file('index.html')
        except werkzeug.exceptions.NotFound:
            log.debug('No index.html found in static folder. Serving backup.')
            # when actinia-metadata-plugin is installed in single mode, the swagger
            # endpoint would be "latest/api/swagger.json". As api docs exist in
            # single mode, use this fallback for plugin mode.
            return ("""<h1 style='color:red'>actinia-metadata-plugin</h1>
                <a href="api/v1/swagger.json">API docs</a>""")

    @app.route('/<path:filename>')
    def static_content(filename):
        # WARNING: all content from folder "static" will be accessible!
        return send_from_directory(app.static_folder, filename)

    apidoc.add_resource(Upload, '/files')

    apidoc.add_resource(GnosConnection, '/metadata/test/connection')

    apidoc.add_resource(RawTags, '/metadata/raw/tags/<tags>')
    apidoc.add_resource(RawCat, '/metadata/raw/categories/<category>')
    apidoc.add_resource(RawUuid, '/metadata/raw/uuids/<uuid>')
    apidoc.add_resource(Tags, '/metadata/geodata/tags/<tags>')
    apidoc.add_resource(Uuid, '/metadata/geodata/uuids/<uuid>')
