"""
api/schemas/diary.py
Transport schemas for Investor Diary endpoints.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ContextualPromptSchema(BaseModel):
    id: str
    trigger_text: str
    question: str
    action_text: str
    action_href: str
    type: str


class DiaryEntryCreateRequest(BaseModel):
    planning_unit_id: str
    date: str
    title: Optional[str] = None
    content: str
    tags: List[str] = Field(default_factory=list)
    prompts: List[ContextualPromptSchema] = Field(default_factory=list)
    follow_up_note: Optional[str] = None
    is_important: bool = False


class DiaryEntryResponse(BaseModel):
    id: str
    planning_unit_id: str
    date: str
    title: Optional[str] = None
    content: str
    tags: List[str] = Field(default_factory=list)
    prompts: List[ContextualPromptSchema] = Field(default_factory=list)
    follow_up_note: Optional[str] = None
    is_important: bool = False
    created_at: str
    updated_at: str


class FinancialDecisionCreateRequest(BaseModel):
    planning_unit_id: str
    date: str
    title: str
    summary: str
    category: str
    source: str
    source_id: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class FinancialDecisionResponse(BaseModel):
    id: str
    planning_unit_id: str
    date: str
    title: str
    summary: str
    category: str
    source: str
    source_id: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None
    created_at: str
    historical: bool = True
