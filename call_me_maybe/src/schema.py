"""Pydantic models for function definitions and results."""

from typing import Literal

from pydantic import BaseModel

ArgType = Literal["number", "integer", "string", "boolean"]
ArgValue = int | float | str | bool


class ParameterSpec(BaseModel):
    """Type specification of a parameter or return value."""

    type: ArgType


class FunctionDefinition(BaseModel):
    """A function the model is allowed to call."""

    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ParameterSpec


class ResultItem(BaseModel):
    """One function call selected for one prompt."""

    prompt: str
    fn_name: str
    args: dict[str, ArgValue]
