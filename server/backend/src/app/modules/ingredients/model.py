import uuid
from typing import Self

import sqlalchemy as sa
from app.core.base_db import BaseDB
from app.core.logger import get_logger
from pydantic import UUID4, BaseModel
from sqlalchemy.dialects.postgresql import UUID

logger = get_logger(__name__)


class IngredientDB(BaseDB):
    __tablename__ = "ingredients"

    primary_key = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(200), nullable=False)


class IngredientDTO(BaseModel):
    name: str
    primary_key: UUID4

    class Config:
        validate_assignment = True
        from_attributes = True


class IngredientResponse(IngredientDTO):
    def from_dto(ingredient: IngredientDTO) -> Self:
        return IngredientResponse(**ingredient.model_dump())
