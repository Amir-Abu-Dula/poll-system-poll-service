from typing import Optional

from pydantic import BaseModel


class Question(BaseModel):
    id: Optional[int] = None
    title: str
    first_option: str
    second_option: str
    third_option: str
    fourth_option: str