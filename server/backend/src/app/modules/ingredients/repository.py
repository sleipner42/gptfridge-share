import json
from typing import List

from app.core.logger import get_logger
from app.core.openai import ContentModel, MessageModel, OpenAiClient, PayLoadModel
from app.modules.image.model import ImageDTO, ImageOut
from app.modules.ingredients.model import IngredientDB, IngredientDTO
from app.settings import settings
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = get_logger(__name__)

PROMPT = """Identify the common eatable food ingredients visible in the picture and list them in JSON format. 
Only include the names of the ingredients in singular in the list, without descriptions or packaging details. 
Go from left to right and from top to bottom. If there are no identifiable food ingredients, provide an empty list. Only a json list and not newlines in the response.
Response format example: ["tomato", "cucumber", "chicken"]"""


class IngredientRepository:
    def __init__(self, open_ai_client: OpenAiClient, session: Session):
        self.open_ai_client = open_ai_client
        self.session = session

    def get_ingredients(self) -> List[IngredientDTO]:
        stmt = select(IngredientDB)
        objs = self.session.execute(stmt).scalars()

        dtos = [IngredientDTO.model_validate(db_obj) for db_obj in objs or []]

        return dtos

    def get_ingredients_with_image(self, image: ImageDTO) -> List[IngredientDTO]:
        contents = [
            ContentModel(type="text", text=PROMPT),
            ContentModel(type="image", image_url=ImageOut.from_dto(image)),
        ]

        messages = MessageModel(content=contents)

        payload = PayLoadModel(messages=[messages])

        if settings.MOCK_OPENAI:
            json_ingredients = ["water", "bulgur"]
        else:
            response = self.open_ai_client.make_request(payload=payload)
            json_ingredients = json.loads(response.choices[0].message.content)
            logger.info(json_ingredients)

        stmt = select(IngredientDB).where(
            IngredientDB.name.in_(
                [obj.lower().replace(" ", "_") for obj in json_ingredients]
            )
        )

        objs = self.session.execute(stmt).all()

        ingredients = [IngredientDTO.model_validate(obj[0]) for obj in objs]

        return ingredients
