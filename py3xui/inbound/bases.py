"""
This module contains a base class for models that have a JSON string field.
"""

import json
from pydantic import BaseModel, model_validator


class JsonStringModel(BaseModel):
    """
    A base class for models that have a JSON string field.
    """
    @model_validator(mode="before")
    def model_validate(cls, values):  # pylint: disable=no-self-argument, arguments-differ
        """
        Validates the input and converts it to a dictionary if it's a JSON string.

        Args:
            values: The input value to be validated.

        Returns:
            The input value converted to a dictionary if it's a JSON string, otherwise returns the input value.
        """
        if isinstance(values, str):
            try:
                return json.loads(values)
            except json.JSONDecodeError:
                pass
        return values