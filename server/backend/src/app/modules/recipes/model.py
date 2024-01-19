import uuid
from typing import List, Self

import sqlalchemy as sa
from app.core.base_db import BaseDB
from app.core.logger import get_logger
from app.modules.ingredients.model import IngredientDB, IngredientDTO
from pydantic import BaseModel, computed_field, field_validator
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

logger = get_logger(__name__)


class Association(BaseDB):
    __tablename__ = "association_table"
    _use_timestamps = False

    recipe_pk = sa.Column(sa.ForeignKey("recipes.primary_key"), primary_key=True)
    ingredient_pk = sa.Column(
        sa.ForeignKey("ingredients.primary_key"), primary_key=True
    )


class RecipeDB(BaseDB):
    __tablename__ = "recipes"

    primary_key: Mapped[uuid.uuid4] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    image_url: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    url: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    ingredients: Mapped[List[IngredientDB]] = relationship(
        secondary=Association.__tablename__,
    )

    @hybrid_property
    def nr_of_ingredients(self) -> int:
        return len(self.ingredients)


class RecipeDTO(BaseModel):
    name: str
    image_url: str
    url: str
    nr_of_ingredients: int

    class Config:
        validate_assignment = True
        from_attributes = True


class RecipeMatchDTO(BaseModel):
    recipe: RecipeDTO
    match: int


class RecipeMatchResponse(RecipeMatchDTO):
    def from_dto(recipe_match: RecipeMatchDTO) -> Self:
        return RecipeMatchResponse(**recipe_match.model_dump())
