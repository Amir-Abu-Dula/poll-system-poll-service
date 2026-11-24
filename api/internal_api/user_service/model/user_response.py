from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    is_registered: bool