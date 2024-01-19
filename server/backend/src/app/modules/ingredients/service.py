from typing import List, Optional, Tuple

from app.modules.image.model import ImageDTO
from app.modules.ingredients.model import IngredientDTO
from app.modules.ingredients.repository import IngredientRepository


class IngredientService:
    repository: IngredientRepository

    def __init__(self, repository: IngredientRepository) -> None:
        self.repository = repository

    def get_ingredients_for_image(self, image: ImageDTO) -> List[IngredientDTO]:
        return self.repository.get_ingredients_with_image(image)

    def get_ingredients_for_images(self, images: List[ImageDTO]) -> List[IngredientDTO]:
        all_ingredients = []
        for image in images:
            all_ingredients += self.get_ingredients_for_image(image=image)

        return all_ingredients
    
    def get_ingredients(self) -> List[IngredientDTO]:
        return self.repository.get_ingredients()
