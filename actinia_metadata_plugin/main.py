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


Application entrypoint. Creates Flask app and swagger docs, adds endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from actinia_metadata_plugin import endpoints
from actinia_metadata_plugin.resources.logging import log

app = Flask(__name__)
CORS(app)

API_VERSION = "v1"

URL_PREFIX = f"/api/{API_VERSION}"

apidoc = Api(
    app,
    title="actinia-metadata-plugin",
    api_spec_url=f'{URL_PREFIX}/swagger',
    schemes=['https', 'http'],
    consumes=['application/json'],
    description="""Contains communication with a metadata catalog via OGC-CSW,
                   in usage with GeoNetwork opensource.
                   """
)

endpoints.create_endpoints(apidoc)


if __name__ == '__main__':
    # call this for development only with
    # `python -m actinia_metadata_plugin.main`
    log.debug('starting app in development mode...')
    app.run(debug=True, use_reloader=False)
    # for production environent use application in wsgy.py
