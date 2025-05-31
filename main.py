from fastapi import FastAPI, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from JWTUtils import create_access_token, get_current_user
from database import get_db
from models.models import User, UserCreate, Token, Section, SectionBase, Note, NoteBase, UserOut, NoteOut, LoginRequest
from services.noteService import NoteService
from services.sectionService import SectionService
from services.userService import UserService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=UserOut)
async def register(user: UserCreate, db=Depends(get_db)):
    """Register a new user."""
    return await UserService.register(db, user)


@app.post("/login", response_model=Token)
async def login(data: LoginRequest, db=Depends(get_db)):
    """Authenticate user and return JWT token."""
    nickname = data.nickname
    password = data.password
    user = await UserService.authenticate(db, nickname, password)
    access_token = create_access_token(data={"sub": str(user['id'])})
    return {"access_token": access_token, "token_type": "Bearer", 'nickname': nickname}


@app.post("/sections", response_model=Section)
async def create_section(section: SectionBase, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Create a new section."""
    return await SectionService.create(db, section, current_user)


@app.get("/sections", response_model=List[Section])
async def get_sections(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Get all sections for the authenticated user."""
    return await SectionService.get_all(db, current_user)


@app.get("/sections/{section_id}", response_model=Section)
async def get_section(section_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Get a specific section."""
    return await SectionService.get(db, section_id, current_user)


@app.put("/sections/{section_id}", response_model=Section)
async def update_section(section_id: UUID, section: SectionBase, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Update a section."""
    return await SectionService.update(db, section_id, section, current_user)


@app.delete("/sections/{section_id}")
async def delete_section(section_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Delete a section."""
    return await SectionService.delete(db, section_id, current_user)


@app.post("/sections/{section_id}/notes", response_model=Note)
async def create_note(section_id: UUID, note: NoteBase, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Create a new note in a section."""
    return await NoteService.create(db, note, section_id, current_user)


@app.get("/sections/{section_id}/notes", response_model=List[NoteOut])
async def get_notes(section_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Get all notes in a section."""
    return await NoteService.get_all(db, section_id, current_user)


@app.get("/sections/{section_id}/notes/{note_id}", response_model=Note)
async def get_note(section_id: UUID, note_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Get a specific note."""
    return await NoteService.get(db, note_id, section_id, current_user)


@app.put("/sections/{section_id}/notes/{note_id}", response_model=Note)
async def update_note(section_id: UUID, note_id: UUID, note: NoteBase, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Update a note."""
    return await NoteService.update(db, note_id, note, section_id, current_user)


@app.delete("/sections/{section_id}/notes/{note_id}")
async def delete_note(section_id: UUID, note_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Delete a note."""
    return await NoteService.delete(db, note_id, section_id, current_user)


@app.get("/notes", response_model=List[NoteOut])
async def get_all_user_notes(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Get all notes across all sections for the authenticated user."""
    return await NoteService.get_all_by_user_id(db, current_user)