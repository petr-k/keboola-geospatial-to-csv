import json
import copy
import os
from jsonschema import Draft4Validator, validators


def _load_schema():
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "parameters-schema.json"
    )
    with open(path) as f:
        return json.load(f)


def _extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


_validator = _extend_with_default(Draft4Validator)(_load_schema())


def validate_expand_defaults(config_parameters):
    cloned_parameters = copy.deepcopy(config_parameters)
    _validator.validate(cloned_parameters)
    return cloned_parameters
