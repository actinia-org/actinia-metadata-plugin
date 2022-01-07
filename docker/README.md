# actinia-metadata-plugin

You can run actinia-metadata-plugin in multiple ways:

* as actinia-core plugin
* as standalone app with gunicorn, connected with a running actinia-core instance

# As actinia-core plugin

To run actinia-metadata-plugin with actinia-core, see https://github.com/mundialis/actinia_core/blob/master/docker/README.md#Local-dev-setup-with-docker
Mind that it needs to be registered in the actinia-core config under API.plugins


# As standalone app

First, build an actinia-metadata-plugin image with source-2-image. Install source-to-image binary (here v1.1.9 was used) and run:
```
git clone git@github.com:mundialis/actinia-metadata-plugin.git
cd actinia-metadata-plugin
docker build docker/s2i-actinia-metadata-builder -t s2i-actinia-metadata-builder
```
__To build actinia-metadata-plugin, run:__
```
s2i build git@github.com:mundialis/actinia-metadata-plugin.git s2i-actinia-metadata-builder actinia-metadata-plugin -e APP_CONFIG=/gunicorn.cfg -c

# if you have local actinia-metadata-plugin changes, run
s2i build . s2i-actinia-metadata-builder actinia-metadata -e APP_CONFIG=/gunicorn.cfg -c

```
__To run actinia-metadata-plugin as standalone app, run__
```
docker-compose --file docker/docker-compose.yml up -d
```

__For actinia-metadata-plugin development, run and enter the running container:__
```
docker-compose --file docker/docker-compose.yml run --rm \
  --service-ports -w /opt/app-root/src --entrypoint bash \
  -v $HOME/workworkwork/repos/actinia/actinia-metadata-plugin/actinia_metadata_plugin:/opt/app-root/src/actinia_metadata_plugin actinia-metadata
```

__Inside the container, run the actinia-metadata-plugin server with mounted source code:__
```
python3 setup.py install
python3 setup.py test

# python3 -m actinia_metadata_plugin.main
gunicorn -b 0.0.0.0:5000 -w 1 --access-logfile=- -k gthread actinia_metadata_plugin.wsgi
```

__And test from outside with API calls, e.g.:__
```
curl 'http://127.0.0.1:5000'
```

## dev notes:

As actinia-metadata-plugin can be run as actinia-core plugin and standalone,
the endpoint classes inherit either from flask_restful's Resource (standalone +
plugin mode) or from the extended actinia-core ResourceBase (only plugin mode).

__build actinia-metadata-plugin from checked out s2i image__
```
cd docker/s2i-actinia-metadata-builder/
git clone git@github.com:sclorg/s2i-python-container.git
cd s2i-python-container
make build TARGET=centos7 VERSIONS=3.6
docker build docker/s2i-actinia-metadata-builder/s2i-python-container/3.6 -t s2i-python-container
```

## Build and run as standalone app without docker:

### Requirements
```
sudo apt install \
    python-virtualenv\
    python3\
    python3-dev\
```
* a running GeoNetwork instance

### Installation
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

## Create API docs
```
API_VERSION="v1" # As standalone app
API_VERSION="v3" # As actinia-core plugin
wget -O /tmp/actinia-metadata.json http://127.0.0.1:5000/api/${API_VERSION}/swagger.json
```
Run spectacle docker image to generate the HTML documentation
```
docker run -v /tmp:/tmp -t sourcey/spectacle \
  spectacle /tmp/actinia-metadata.json -t /tmp

# or if you have spectacle installed (npm install -g spectacle-docs), run
cd actinia_metadata_plugin/static
spectacle /tmp/actinia-metadata.json -t .

# to build all in one file:
spectacle -1 /tmp/actinia-metadata.json -t .
```
beautify css
```
sed -i 's+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />\n    <link rel="stylesheet" href="stylesheets/actinia.css" />+g' index.html
```
