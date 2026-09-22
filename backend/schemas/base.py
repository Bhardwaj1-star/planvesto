from pydantic import BaseModel, ConfigDict


class StrictRequestModel(BaseModel):
    """Base class for API request bodies: reject unknown fields instead of silently ignoring them."""

    model_config = ConfigDict(extra="forbid")
