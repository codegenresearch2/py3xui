import json
from pydantic import BaseModel, model_validator


class JsonStringModel(BaseModel):
    """
    A model that validates whether the input is a JSON string and converts it to a dictionary if possible.
    """

    @model_validator(mode="before")
    def model_validate(cls, values):  # pylint: disable=no-self-argument, arguments-differ
        """
        Validates the input and converts it to a dictionary if it's a JSON string.

        Args:
            values: The input value to be validated.

        Returns:
            The input value converted to a dictionary if it's a JSON string, otherwise the input value.
        """
        if isinstance(values, str):
            try:
                return json.loads(values)
            except json.JSONDecodeError:
                pass
        return values