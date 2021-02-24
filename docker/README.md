You can run actinia-metadata-plugin in multiple ways:

* as actinia-core plugin
* as standalone app with gunicorn, connected with a running actinia-core instance

Depending on how you run, it, actinia-metadata-plugin has different endpoints as some make only sense in plugin mode or vice versa. See `actinia_metadata_plugin/endpoints.py`. Therefore a running postgres instance is only needed in standalone mode. If used as actinia-core plugin, the main.py is not executed.


# As actinia-core plugin

To run actinia-metadata-plugin with actinia-core, see https://github.com/mundialis/actinia_core/blob/master/docker/README.md#Local-dev-setup-with-docker


# As standalone app

First, build an actinia-metadata-plugin image with source-2-image. Install source-to-image binary (here v1.1.9 was used) and run:
```
docker build docker/s2i-actinia-metadata-plugin-builder -t s2i-actinia-metadata-plugin-builder
```
__To update actinia-metadata-plugin, run:__
```
s2i build git@github.com:mundialis/actinia-metadata-plugin.git s2i-actinia-metadata-plugin-builder actinia-metadata-plugin -e APP_CONFIG=/gunicorn.cfg -c

# if you have local actinia-metadata-plugin changes, run
# s2i build actinia-metadata-plugin s2i-actinia-metadata-plugin-builder actinia-metadata-plugin -e APP_CONFIG=/gunicorn.cfg -c

```
__To run actinia-metadata-plugin as standalone app, run__
```
docker-compose --file docker/docker-compose.yml up -d
```

__For actinia-metadata-plugin development, run and enter the running container:__
```
docker-compose --file docker/docker-compose.yml up -d postgis

docker-compose --file docker/docker-compose.yml run --rm \
  --service-ports -w /opt/app-root/src --entrypoint bash \
  -v $HOME/repos/actinia/actinia-metadata-plugin/actinia_metadata_plugin:/opt/app-root/src/actinia_metadata_plugin actinia-metadata-plugin
```

__Inside the container, run the actinia-metadata-plugin server with mounted source code:__
```
python3 setup.py install

# python3 -m actinia_metadata_plugin.main
gunicorn -b 0.0.0.0:5000 -w 1 --access-logfile=- -k gthread actinia_metadata_plugin.wsgi
```

__And test from outside with API calls, e.g.:__
```
curl 'http://127.0.0.1:5000'
```


## dev notes:

As actinia-metadata-plugin can be run as actinia-core plugin and standalone, the endpoint
classes inherit either from flask_restful's Resource (standalone + plugin mode) or from the extended actinia-core ResourceBase (only plugin mode).

__build actinia-metadata-plugin from checked out s2i image__
```
cd docker/s2i-actinia-metadata-plugin-builder/
git clone git@github.com:sclorg/s2i-python-container.git
cd s2i-python-container
make build TARGET=centos7 VERSIONS=3.6
docker build docker/s2i-actinia-metadata-plugin-builder/s2i-python-container/3.6 -t s2i-python-container
```


__test process chains in actinia-core:__
```
curl -u actinia-metadata-plugin:actinia-metadata-plugin 'http://127.0.0.1:8088/api/v1/locations'

JSON=pc.json
curl -u actinia-metadata-plugin:actinia-metadata-plugin -X POST "http://127.0.0.1:8088/api/v1/locations/nc_spm_08/processing_async_export" \
     -H 'accept: application/json' -H 'Content-Type: application/json' -d @$JSON \
     | json urls.status | xargs curl -u actinia-metadata-plugin:actinia-metadata-plugin -X GET

curl -u actinia-metadata-plugin:actinia-metadata-plugin -X POST "http://127.0.0.1:8088/api/v1/locations/mynewlocation" -H 'accept: application/json' -H \
  'Content-Type: application/json' -d '{"epsg": "25832"}'
```

__copy paste for dev__
```

docker-compose --file docker/docker-compose-plugin.yml run --rm \
  --service-ports -w /src/actinia-metadata-plugin --entrypoint bash \
  -v $HOME/repos/actinia/actinia_core/src:/src/actinia_core/src \
  -v $HOME/repos/actinia/actinia-metadata-plugin/actinia_metadata_plugin:/src/actinia-metadata-plugin/actinia_metadata_plugin actinia-core

bash /src/start-dev.sh

(cd /src/actinia_core && python3 setup.py install) && \
    python3 setup.py install && \
    gunicorn -b 0.0.0.0:8088 -w 1 --access-logfile=- -k gthread actinia_core.main:flask_app


```



## As standalone app without docker

###Requirements
```
sudo apt install \
    python-virtualenv\
    python3\
    python3-dev\
```
* a running GeoNetwork instance
* a running PostgreSQL instance

### DEV - Installation
For local developments outside of docker, it is preferred to run actinia-metadata-plugin in a virtual python environment.

Clone repository, create virtual environment and activate it:
```
git clone git@github.com:mundialis/actinia-metadata-plugin.git
cd actinia-metadata-plugin
virtualenv -p python3 venv
. venv/bin/activate
```

Change configuration in ```config/mount```

Install required Python packages into the virtual environment:
```
pip install -r requirements.txt
python setup.py install
```
Run tests:
```
python setup.py test
```

Run the server for development:
```
python -m actinia_metadata_plugin.main
```

Or for production use actinia_metadata_plugin.wsgi as WSGI callable:
```
gunicorn -b :5000 -w 1 --access-logfile=- -k gthread actinia_metadata_plugin.wsgi

```

If all done, leave environment
```
deactivate
```

## As standalone app with s2i (e.g. for INT - Installation)

```
git clone git@github.com:mundialis/actinia-metadata-plugin.git
cd actinia-metadata-plugin
docker build s2i-actinia-metadata-plugin-builder -t s2i-actinia-metadata-plugin-builder
s2i build . s2i-actinia-metadata-plugin-builder actinia-metadata-plugin
docker-compose -f ~/docker/docker-compose.yml up -d actinia-metadata-plugin
```

__INT - Update__

```
cd actinia-metadata-plugin
s2i build . s2i-actinia-metadata-plugin-builder actinia-metadata-plugin

docker-compose -f ~/docker/docker-compose.yml up -d actinia-metadata-plugin
```


##

__test new__
```
http://127.0.0.1:8088/api/v1/grassmodules
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale3

http://127.0.0.1:8088/api/v1/actiniamodules
http://127.0.0.1:8088/api/v1/actiniamodules/vector_area

http://127.0.0.1:8088/api/v1/modules
http://127.0.0.1:8088/api/v1/modules/d.barscale
http://127.0.0.1:8088/api/v1/modules/vector_area
http://127.0.0.1:8088/api/v1/modules/vector_area5

http://127.0.0.1:8088/api/v1/swagger.json

```

## manual build to dockerhub

Only for latest image. Checkout and pull master branch and make sure you don't
have any local changes.
```
docker build -f docker/actinia-core/Dockerfile -t actini-gdi:latest .
docker tag f6865645c733 mundialis/actinia-metadata-plugin:latest
docker push mundialis/actinia-metadata-plugin:latest
```
