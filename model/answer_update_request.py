from pydantic import BaseModel

from model.answer import SelectedOption


class AnswerUpdateRequest(BaseModel):
    selected_option: SelectedOption