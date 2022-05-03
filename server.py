#! /usr/bin/env python3

import click

from flask import Flask, request, abort

import yaml


app = Flask(__name__)


def parse_yaml(path: str):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return data


@app.route("/")
def index():
    data = parse_yaml(app.config["config_file"])

    def get_request_arg(key: str):
        try:
            return request.args[key]
        except KeyError:
            abort(400, f"arg missing: {key}")

    for system in data["clientupdater_systems"]:
        if system["name"] == get_request_arg("oem"):
            break
    else:
        abort(500, "no such oem")

    platform_name = get_request_arg("platform")

    alias_platforms = dict([i.split("=") for i in system.get("alias_platforms", [])])

    try:
        platform_name = alias_platforms[platform_name]
    except KeyError:
        pass

    for platform in system["platforms"]:
        if platform_name == platform["name"]:
            break
    else:
        abort(500, "no such platform")

    assert get_request_arg("version")
    assert get_request_arg("buildArch") == "x86_64"
    assert get_request_arg("currentArch") == "x86_64"
    assert get_request_arg("versionsuffix") is not None

    try:
        xml = f"""\
<?xml version="1.0"?>
<owncloudclient>
  <version>{platform["current_version"]}</version>
  <versionstring>{platform["current_version_string"]}</versionstring>
  <web></web>
  <downloadurl>{platform["download_url"]}</downloadurl>
</owncloudclient>
"""
    except KeyError as e:
        print(repr(e))
        abort(500, repr(e))

    return app.response_class(xml, headers={"Content-Type": "text/xml"})


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
def main(config_file: str):
    app.config["config_file"] = config_file

    app.run(debug=True)


if __name__ == "__main__":
    main()
