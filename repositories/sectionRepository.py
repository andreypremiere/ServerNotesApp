from uuid import UUID
from models.models import SectionBase


class SectionRepository:
    @staticmethod
    async def create(db, section: SectionBase, user_id: UUID):
        """Create a new section for a user."""
        return await db.fetchrow(
            "INSERT INTO sections (user_id, title, subtitle) VALUES ($1, $2, $3) RETURNING *",
            user_id, section.title, section.subtitle
        )

    @staticmethod
    async def get_all(db, user_id: UUID):
        """Get all sections for a user."""
        return await db.fetch("SELECT * FROM sections WHERE user_id = $1", user_id)

    @staticmethod
    async def get(db, section_id: UUID, user_id: UUID):
        """Get a specific section by ID."""
        return await db.fetchrow(
            "SELECT * FROM sections WHERE id = $1 AND user_id = $2", section_id, user_id
        )

    @staticmethod
    async def update(db, section_id: UUID, section: SectionBase, user_id: UUID):
        """Update a section."""
        return await db.fetchrow(
            "UPDATE sections SET title = $1, subtitle = $2 WHERE id = $3 AND user_id = $4 RETURNING *",
            section.title, section.subtitle, section_id, user_id
        )

    @staticmethod
    async def delete(db, section_id: UUID, user_id: UUID):
        """Delete a section."""
        return await db.execute(
            "DELETE FROM sections WHERE id = $1 AND user_id = $2", section_id, user_id
        )