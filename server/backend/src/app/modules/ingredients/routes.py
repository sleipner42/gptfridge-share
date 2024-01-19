from typing import List

from app.core.base_response import BaseResponse
from app.core.db_session import get_db_session
from app.core.logger import Logger, get_logger
from app.core.openai import OpenAiClient, get_openai_client
from app.modules.image.model import ImageDTO, ImageIn
from app.modules.ingredients.model import IngredientResponse
from app.modules.ingredients.repository import IngredientRepository
from app.modules.ingredients.service import IngredientService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
logger: Logger = get_logger(__name__)


@router.post(
    "/image",
    response_model=BaseResponse[List[IngredientResponse]],
    tags=["ingredients"],
)
def get_ingredients_image(
    images: List[ImageIn],
    open_ai_client: OpenAiClient = Depends(get_openai_client),
    session: Session = Depends(get_db_session),
) -> BaseResponse[str]:
    images_dto = [ImageDTO.from_image_in(image) for image in images]

    # Repository Layer: Fetch list from Database
    ingredients = IngredientService(
        repository=IngredientRepository(open_ai_client=open_ai_client, session=session)
    ).get_ingredients_for_images(images=images_dto)

    # Route Response: Transform datamodel to response model(s)
    response_data = [
        IngredientResponse.from_dto(ingredient) for ingredient in ingredients
    ]

    return BaseResponse(data=response_data)


@router.get(
    "/",
    response_model=BaseResponse[List[IngredientResponse]],
    tags=["ingredients"],
)
async def get_ingredients(
    open_ai_client: OpenAiClient = Depends(get_openai_client),
    session: Session = Depends(get_db_session),
) -> BaseResponse[str]:
    # Repository Layer: Fetch list from Database
    ingredients = IngredientService(
        repository=IngredientRepository(open_ai_client=open_ai_client, session=session)
    ).get_ingredients()

    # Route Response: Transform datamodel to response model(s)
    response_data = [
        IngredientResponse.from_dto(ingredient) for ingredient in ingredients
    ]

    return BaseResponse(data=response_data)
