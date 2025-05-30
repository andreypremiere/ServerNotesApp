from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    password: str


class UserOut(BaseModel):
    id: UUID
    nickname: str


class User(UserBase):
    id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class SectionBase(BaseModel):
    title: str
    subtitle: Optional[str] = None


class Section(SectionBase):
    id: UUID
    user_id: UUID


class SectionOut(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    subtitle: str


class NoteBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None
    map: Optional[dict] = None


class Note(NoteBase):
    id: UUID
    section_id: UUID


class NoteOut(BaseModel):
    id: UUID
    section_id: UUID
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None
    map: Optional[dict] = None
