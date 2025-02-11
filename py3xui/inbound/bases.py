"""
This module contains base classes for models that include a JSON string field.
"""

import json
from pydantic import BaseModel, model_validator


class JsonStringModel(BaseModel):
    """
    Base class for models that include a JSON string field.
    """

    @model_validator(mode="before")
    def model_validate(cls, values):  # pylint: disable=no-self-argument, arguments-differ
        """
        Validates the input values. If the input is a string, it attempts to parse it as JSON.

        Args:
            values: The input values to validate.

        Returns:
            The parsed JSON object if the input is a string, otherwise the input values.
        """
        if isinstance(values, str):
            try:
                return json.loads(values)
            except json.JSONDecodeError:
                pass
        return values