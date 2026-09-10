from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


DiaryCategory = Literal["Strategy", "Investment", "Debt", "Goal", "Allocation", "General"]
DiaryPromptType = Literal["goal", "strategy", "liability", "investment", "budget"]


class ContextualPrompt(BaseModel):
    id: str
    trigger_text: str
    question: str
    action_text: str
    action_href: str
    type: DiaryPromptType


class DiaryEntry(BaseModel):
    id: str | None = None
    planning_unit_id: str
    date: str
    title: str | None = None
    content: str
    tags: list[str] = Field(default_factory=list)
    prompts: list[ContextualPrompt] = Field(default_factory=list)
    follow_up_note: str | None = None
    is_important: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_required_fields(self) -> "DiaryEntry":
        if not self.planning_unit_id.strip():
            raise ValueError("planning_unit_id cannot be empty")
        if not self.content.strip():
            raise ValueError("content cannot be empty")
        return self


class FinancialDecision(BaseModel):
    id: str | None = None
    planning_unit_id: str
    date: str
    title: str
    summary: str
    category: DiaryCategory
    source: str
    source_id: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    historical: bool = True

    @model_validator(mode="after")
    def validate_required_fields(self) -> "FinancialDecision":
        if not self.planning_unit_id.strip():
            raise ValueError("planning_unit_id cannot be empty")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.summary.strip():
            raise ValueError("summary cannot be empty")
        return self
