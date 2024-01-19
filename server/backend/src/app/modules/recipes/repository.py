from typing import List

from app.core.logger import get_logger
from app.modules.ingredients.model import IngredientDB
from app.modules.recipes.model import Association, RecipeDB, RecipeDTO, RecipeMatchDTO
from pydantic import UUID4
from sqlalchemy import func, select
from sqlalchemy.orm import Session

logger = get_logger(__name__)


class RecipeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_recipes(self, ingredients_pks: List[UUID4]) -> List[RecipeMatchDTO]:
        stmt = (
            select(RecipeDB, func.count(Association.ingredient_pk))
            .join(RecipeDB)
            .where(Association.recipe_pk == RecipeDB.primary_key)
            .join(IngredientDB)
            .where(Association.ingredient_pk.in_(ingredients_pks))
            .group_by(RecipeDB)
            .order_by(func.count(Association.ingredient_pk).desc())
            .limit(50)
        )

        objs = self.session.execute(stmt).all()

        dtos = [
            RecipeMatchDTO(
                recipe=RecipeDTO.model_validate(db_obj[0]),
                match=db_obj[1],
            )
            for db_obj in objs or []
        ]

        return dtos
