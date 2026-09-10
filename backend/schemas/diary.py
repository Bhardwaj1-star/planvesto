from typing import Any

from pydantic import BaseModel, Field

from models.diary import ContextualPrompt, DiaryCategory


class DiaryEntryCreateRequest(BaseModel):
    planning_unit_id: str
    date: str
    title: str | None = None
    content: str
    tags: list[str] = Field(default_factory=list)
    prompts: list[ContextualPrompt] = Field(default_factory=list)
    follow_up_note: str | None = None
    is_important: bool = False


class DiaryEntryUpdateRequest(BaseModel):
    date: str | None = None
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    prompts: list[ContextualPrompt] | None = None
    follow_up_note: str | None = None
    is_important: bool | None = None


class FinancialDecisionCreateRequest(BaseModel):
    planning_unit_id: str
    date: str
    title: str
    summary: str
    category: DiaryCategory
    source: str
    source_id: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
