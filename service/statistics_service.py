from typing import Dict, List, Optional

from model.answer import Answer, SelectedOption
from model.question import Question
from model.statistics_response import (
    OptionCount,
    QuestionAnswersCountResponse,
    QuestionResultsResponse,
    UserAnswerResponse,
    UserAnswersCountResponse,
    UserAnswersResponse,
)
from repository import answer_repository, question_repository
from service import question_service


def _option_text(question: Question, option: SelectedOption) -> str:
    option_texts: Dict[SelectedOption, str] = {
        SelectedOption.FIRST: question.first_option,
        SelectedOption.SECOND: question.second_option,
        SelectedOption.THIRD: question.third_option,
        SelectedOption.FOURTH: question.fourth_option
    }
    return option_texts[option]


def _build_question_results(question: Question, counts: Dict[str, int]) -> QuestionResultsResponse:
    options: List[OptionCount] = []
    for option in SelectedOption:
        options.append(
            OptionCount(
                option=option,
                option_text=_option_text(question, option),
                count=counts.get(option.name, 0)
            )
        )

    return QuestionResultsResponse(
        question_id=question.id,
        question_title=question.title,
        options=options,
        total_answers=sum(option_count.count for option_count in options)
    )


async def get_question_results(question_id: int) -> QuestionResultsResponse:
    question: Question = await question_service.get_question_by_id(question_id)
    counts: Dict[str, int] = await answer_repository.count_answers_by_option(question_id)
    return _build_question_results(question, counts)


async def get_question_answers_count(question_id: int) -> QuestionAnswersCountResponse:
    await question_service.get_question_by_id(question_id)
    total_answers: int = await answer_repository.count_answers_by_question_id(question_id)
    return QuestionAnswersCountResponse(question_id=question_id, total_answers=total_answers)


async def get_user_answers(user_id: int) -> UserAnswersResponse:
    answers: List[Answer] = await answer_repository.get_answers_by_user_id(user_id)
    questions: List[Question] = await question_repository.get_all_questions()
    questions_by_id: Dict[int, Question] = {question.id: question for question in questions}

    user_answers: List[UserAnswerResponse] = []
    for answer in answers:
        question: Optional[Question] = questions_by_id.get(answer.question_id)
        if question is None:
            continue
        user_answers.append(
            UserAnswerResponse(
                question_id=answer.question_id,
                question_title=question.title,
                selected_option=answer.selected_option,
                selected_option_text=_option_text(question, answer.selected_option)
            )
        )

    return UserAnswersResponse(
        user_id=user_id,
        answers=user_answers,
        total_answered=len(user_answers)
    )


async def get_user_answers_count(user_id: int) -> UserAnswersCountResponse:
    total_answered: int = await answer_repository.count_answers_by_user_id(user_id)
    return UserAnswersCountResponse(user_id=user_id, total_answered=total_answered)


async def get_all_questions_results() -> List[QuestionResultsResponse]:
    questions: List[Question] = await question_repository.get_all_questions()
    all_counts: Dict[int, Dict[str, int]] = await answer_repository.count_all_answers_by_question_and_option()

    return [
        _build_question_results(question, all_counts.get(question.id, {}))
        for question in questions
    ]