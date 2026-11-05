from typing import Any

from pydantic import Field
from models.diary import ContextualPrompt, DiaryCategory
from schemas.base import StrictRequestModel


class DiaryEntryCreateRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    date: str = Field(min_length=1, max_length=40)
    title: str | None = Field(default=None, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    tags: list[str] = Field(default_factory=list, max_length=30)
    prompts: list[ContextualPrompt] = Field(default_factory=list, max_length=20)
    follow_up_note: str | None = Field(default=None, max_length=2000)
    is_important: bool = False


class DiaryEntryUpdateRequest(StrictRequestModel):
    date: str | None = Field(default=None, max_length=40)
    title: str | None = Field(default=None, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=10000)
    tags: list[str] | None = Field(default=None, max_length=30)
    prompts: list[ContextualPrompt] | None = Field(default=None, max_length=20)
    follow_up_note: str | None = Field(default=None, max_length=2000)
    is_important: bool | None = None


class FinancialDecisionCreateRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    date: str = Field(min_length=1, max_length=40)
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=5000)
    category: DiaryCategory
    source: str = Field(min_length=1, max_length=100)
    source_id: str | None = Field(default=None, min_length=1, max_length=100)
    metrics: dict[str, Any] = Field(default_factory=dict, max_length=50)
    notes: str | None = Field(default=None, max_length=5000)
