from typing import List

from pydantic import BaseModel

from model.answer import SelectedOption


class OptionCount(BaseModel):
    option: SelectedOption
    option_text: str
    count: int


class QuestionResultsResponse(BaseModel):
    question_id: int
    question_title: str
    options: List[OptionCount]
    total_answers: int


class QuestionAnswersCountResponse(BaseModel):
    question_id: int
    total_answers: int


class UserAnswerResponse(BaseModel):
    question_id: int
    question_title: str
    selected_option: SelectedOption
    selected_option_text: str


class UserAnswersCountResponse(BaseModel):
    user_id: int
    total_answered: int


class UserAnswersResponse(BaseModel):
    user_id: int
    answers: List[UserAnswerResponse]
    total_answered: int