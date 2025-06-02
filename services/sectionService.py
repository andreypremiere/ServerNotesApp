from uuid import UUID
from fastapi import HTTPException
from typing import List

from models.models import SectionBase, User, SectionOut, SectionCreate
from repositories.sectionRepository import SectionRepository


class SectionService:
    @staticmethod
    async def create(db, section: SectionCreate, current_user: User) -> SectionOut:
        """Create a new section for the authenticated user."""
        created_section = await SectionRepository.create(db, section, current_user.id)
        return SectionOut(**dict(created_section))

    @staticmethod
    async def get_all(db, current_user: User) -> List[SectionOut]:
        """Get all sections for the authenticated user."""
        sections = await SectionRepository.get_all(db, current_user.id)
        # sections — это список asyncpg.Record, конвертируем каждый в SectionOut
        return [SectionOut(**dict(section)) for section in sections]

    @staticmethod
    async def get(db, section_id: UUID, current_user: User) -> SectionOut:
        """Get a specific section for the authenticated user."""
        section = await SectionRepository.get(db, section_id, current_user.id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        return SectionOut(**dict(section))

    @staticmethod
    async def update(db, section_id: UUID, section: SectionBase, current_user: User) -> SectionOut:
        """Update a section for the authenticated user."""
        updated_section = await SectionRepository.update(db, section_id, section, current_user.id)
        if not updated_section:
            raise HTTPException(status_code=404, detail="Section not found")
        return SectionOut(**dict(updated_section))

    @staticmethod
    async def delete(db, section_id: UUID, current_user: User):
        """Delete a section for the authenticated user."""
        result = await SectionRepository.delete(db, section_id, current_user.id)
        if result == 0:
            raise HTTPException(status_code=404, detail="Section not found")
        return {"message": "Section deleted"}
