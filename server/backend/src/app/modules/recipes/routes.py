from typing import List

from app.core.base_response import BaseResponse
from app.core.db_session import get_db_session
from app.core.logger import Logger, get_logger
from app.modules.recipes.model import RecipeMatchResponse
from app.modules.recipes.repository import RecipeRepository
from app.modules.recipes.service import RecipeService
from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

router = APIRouter()
logger: Logger = get_logger(__name__)


@router.post(
    "/",
    response_model=BaseResponse[List[RecipeMatchResponse]],
    tags=["recipes"],
)
def get_recipes(
    ingredients: List[UUID4], session: Session = Depends(get_db_session)
) -> BaseResponse[str]:
    # Repository Layer: Fetch list from Database
    recipe_matches = RecipeService(
        repository=RecipeRepository(session=session)
    ).get_recipes(ingredients_pks=ingredients)

    # Route Response: Transform datamodel to response model(s)
    response_data = [
        RecipeMatchResponse.from_dto(recipe_match) for recipe_match in recipe_matches
    ]

    return BaseResponse(data=response_data)
