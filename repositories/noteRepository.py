import json
from uuid import UUID

from models.models import NoteBase, NoteCreate


class NoteRepository:
    @staticmethod
    async def create(db, note: NoteCreate, section_id: UUID):
        """Create a new note in a section."""
        serialized_map = json.dumps(note.map) if note.map is not None else None
        if note.id:
            return await db.fetchrow(
                "INSERT INTO notes (id, section_id, title, subtitle, content, map) VALUES ($1, $2, $3, $4, $5, "
                "$6) RETURNING *",
                note.id, section_id, note.title, note.subtitle, note.content, serialized_map
            )
        else:
            print('Сработал метод без id')
            return await db.fetchrow(
                "INSERT INTO notes (section_id, title, subtitle, content, map) VALUES ($1, $2, $3, $4, $5) RETURNING *",
                section_id, note.title, note.subtitle, note.content, serialized_map
            )

    @staticmethod
    async def update(db, note_id: UUID, note: NoteBase, section_id: UUID):
        """Update a note."""
        serialized_map = json.dumps(note.map) if note.map is not None else None
        return await db.fetchrow(
            "UPDATE notes SET title = $1, subtitle = $2, content = $3, map = $4 WHERE id = $5 AND section_id = $6 RETURNING *",
            note.title, note.subtitle, note.content, serialized_map, note_id, section_id
        )

    @staticmethod
    async def get_all(db, section_id: UUID):
        """Get all notes in a section."""
        return await db.fetch("SELECT * FROM notes WHERE section_id = $1", section_id)

    @staticmethod
    async def get(db, note_id: UUID, section_id: UUID):
        """Get a specific note by ID."""
        return await db.fetchrow(
            "SELECT * FROM notes WHERE id = $1 AND section_id = $2", note_id, section_id
        )

    @staticmethod
    async def delete(db, note_id: UUID, section_id: UUID):
        """Delete a note."""
        return await db.execute(
            "DELETE FROM notes WHERE id = $1 AND section_id = $2", note_id, section_id
        )

    @staticmethod
    async def get_all_by_user_id(db, user_id: UUID):
        """Get all notes for a specific user across all sections."""
        return await db.fetch(
            """
            SELECT notes.*
            FROM notes
            JOIN sections ON notes.section_id = sections.id
            WHERE sections.user_id = $1
            """,
            user_id
        )
