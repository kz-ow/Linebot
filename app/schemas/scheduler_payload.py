# app/schemas/scheduler_payload.py
from pydantic import BaseModel, validator

class SchedulerPayload(BaseModel):
    scheduler: bool
    endpointUrl: str
    
    @validator("scheduler")
    def check_scheduler(cls, scheduler: bool) -> bool:
        if not isinstance(scheduler, bool):
            raise ValueError(f"invalid scheduler: {scheduler}")
        else:
            return scheduler
    
    @validator("endpointUrl")
    def check_endpointUrl(cls, endpointUrl: str) -> str:
        is_valid = endpointUrl.startswith("https://")
        if not is_valid:
            raise ValueError(f"invalid endpointUrl: {endpointUrl}")
        else:
            return endpointUrl