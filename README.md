# actinia-metadata-plugin

You can run actinia-metadata-plugin in multiple ways:

* as actinia-core plugin
* as standalone app with gunicorn, connected with a running actinia-core instance

If used as actinia-core plugin, the main.py is not executed.

## Installation
For installation or DEV setup, see docker/README.md.

## DEV notes:

### Build

__insprired by https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/__

to create a shippable wheel, run
```
pip3 install --upgrade pip pep517
python3 -m pep517.build .
```

#### Versioning:

https://semver.org/ (MAJOR.MINOR.PATCH)

#### Logging:
in any module, import `from actinia_metadata_plugin.resources.logging import log` and call logger with `log.info("my info i want to log")`
