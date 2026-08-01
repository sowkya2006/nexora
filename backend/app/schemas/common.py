from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str
    status: str = "placeholder"


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
