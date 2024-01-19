from typing import List

from app.modules.recipes.model import RecipeMatchDTO
from app.modules.recipes.repository import RecipeRepository
from pydantic import UUID4


class RecipeService:
    repository: RecipeRepository

    def __init__(self, repository: RecipeRepository) -> None:
        self.repository = repository

    def get_recipes(self, ingredients_pks: List[UUID4]) -> List[RecipeMatchDTO]:
        return self.repository.get_recipes(ingredients_pks=ingredients_pks)
