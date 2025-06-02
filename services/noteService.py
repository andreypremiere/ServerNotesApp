import json
from uuid import UUID
from fastapi import HTTPException
from models.models import NoteBase, NoteOut, User, NoteCreate
from repositories.noteRepository import NoteRepository
from repositories.sectionRepository import SectionRepository


class NoteService:
    @staticmethod
    def _parse_note(note_row) -> NoteOut:
        """Преобразует строку из БД в NoteOut, десериализуя поле map."""
        note_data = dict(note_row)
        if isinstance(note_data.get("map"), str):
            try:
                note_data["map"] = json.loads(note_data["map"])
            except json.JSONDecodeError:
                note_data["map"] = None
        return NoteOut(**note_data)

    @staticmethod
    async def get_all_by_user_id(db, current_user: User):
        """Get all notes across all sections for the authenticated user."""
        notes = await NoteRepository.get_all_by_user_id(db, current_user.id)
        return [NoteService._parse_note(note) for note in notes]

    @staticmethod
    async def create(db, note: NoteCreate, section_id: UUID, current_user: User):
        """Create a new note in a section for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        created_note = await NoteRepository.create(db, note, section_id)
        return NoteService._parse_note(created_note)

    @staticmethod
    async def get_all(db, section_id: UUID, current_user: User):
        """Get all notes in a section for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        notes = await NoteRepository.get_all(db, section_id)
        return [NoteService._parse_note(note) for note in notes]

    @staticmethod
    async def get(db, note_id: UUID, section_id: UUID, current_user: User):
        """Get a specific note for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        note = await NoteRepository.get(db, note_id, section_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        return NoteService._parse_note(note)

    @staticmethod
    async def update(db, note_id: UUID, note: NoteBase, section_id: UUID, current_user: User):
        """Update a note for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        updated_note = await NoteRepository.update(db, note_id, note, section_id)
        if not updated_note:
            raise HTTPException(status_code=404, detail="Note not found")

        return NoteService._parse_note(updated_note)

    @staticmethod
    async def delete(db, note_id: UUID, section_id: UUID, current_user: User):
        """Delete a note for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        result = await NoteRepository.delete(db, note_id, section_id)
        if result == 0:
            raise HTTPException(status_code=404, detail="Note not found")

        return {"message": "Note deleted"}
