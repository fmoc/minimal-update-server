# Minimal ownCloud update server

## Installation

This project uses [Poetry](https://python-poetry.org) to manage its dependencies. Please refer to the [Poetry installation guide](https://python-poetry.org/docs/#installation)

After installing Poetry, you need to create the [virtual environment](https://docs.python.org/3/library/venv.html) and install the dependencies:

```sh
> poetry install
```


## Configuration

The server expects an [ownCloud client update server](https://github.com/owncloud/client-updater-server) YAML configuration file to be passed as a commandline parameter.

A minimal working configuration suitable for testing AppImage update support is provided in the file `clientupdater.yml.example`. Please copy this file prior to first use and adjust it to your needs.


## Run development server

Running the server is easy:

```shell
> poetry run python server.py clientupdater.yml
```

The development server will be spawned on http://127.0.0.1:5000.


## Use from ownCloud client

The [ownCloud desktop client](https://github.com/owncloud/client) can use a custom update server URL. To make use of this feature, you need to set the `OCC_UPDATE_URL` environment variable.

To use the client with this minimal update server, the variable needs to be set accordingly: `export OCC_UPDATE_URL=http://127.0.0.1:5000/`.
