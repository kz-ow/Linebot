# app/schemas/mode_payload.py
from pydantic import BaseModel, validator

class ModePayload(BaseModel):
    mode: str

    @validator("mode")
    def check_endpointUrl(cls, mode: str) -> str:
        is_valid = mode in ["news", "general"]
        if not is_valid:
            raise ValueError(f"invalid mode: {mode}")
        else:
            return mode