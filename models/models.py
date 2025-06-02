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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    nickname: str


class SectionBase(BaseModel):
    title: str
    subtitle: Optional[str] = None


class Section(SectionBase):
    id: UUID
    user_id: UUID


class SectionCreate(BaseModel):
    id: Optional[UUID] = None
    title: str
    subtitle: str


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


class NoteCreate(BaseModel):
    id: Optional[UUID] = None
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None
    map: Optional[dict] = None


class NoteOut(BaseModel):
    id: UUID
    section_id: UUID
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None
    map: Optional[dict] = None


class LoginRequest(BaseModel):
    nickname: str
    password: str
