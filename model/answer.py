from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SelectedOption(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"
    FOURTH = "FOURTH"


class Answer(BaseModel):
    id: Optional[int] = None
    question_id: int
    user_id: int
    selected_option: SelectedOption