# app/schemas/scheduler_payload.py
from pydantic import BaseModel, root_validator

class SchedulerPayload(BaseModel):
    scheduler: bool
    endpointUrl: str | None = None

    @root_validator(skip_on_failure=True)
    def check_endpoint_when_enabled(cls, values):
        scheduler = values.get("scheduler")
        endpoint = values.get("endpointUrl")
        if scheduler:
            if not endpoint or not endpoint.startswith("https://"):
                raise ValueError(f"invalid endpointUrl: {endpoint}")
        return values
        
    