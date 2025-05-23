"""
Pydantic schema for question and answer exchange.
"""

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
