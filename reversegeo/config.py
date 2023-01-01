import argparse
import json

from jsonschema import Draft4Validator, validate

_API = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
        },
        "result_type": {
            "type": "string",
        },
        "key": {
            "type": "string",
        },
    },
    "required": [
        "url",
        "key",
        "result_type",
    ],
    "additionalProperties": False,
}

_HTTP = {
    "type": "object",
    "properties": {
        "timeout": {
            "type": "number",
        },
        "retries": {
            "type": "number",
        },
        "delay": {
            "type": "number",
        },
    },
    "additionalProperties": False,
}

_LOGGING = {
    "type": "object",
    "properties": {
        "log_file_name": {
            "type": "string",
        },
        "logdir": {
            "type": "string",
        },
    },
    "additionalProperties": False,
}

_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "api": _API,
        "http": _HTTP,
        "logging": _LOGGING,
    },
    "required": ["api"],
    "additionalProperties": False,
}


class ConfigValidator(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        json_string = values.read()
        if not json_string:
            raise ValueError("file: {} is empty".format(values.name))
        else:
            config = json.loads(json_string)
            validate(config, _CONFIG_SCHEMA, cls=Draft4Validator)
            setattr(namespace, self.dest, json_string)
