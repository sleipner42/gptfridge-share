from typing import Generator, List, Optional

import requests
from app.core.logger import Logger, get_logger
from app.modules.image.model import ImageOut
from app.settings import settings
from pydantic import BaseModel

logger: Logger = get_logger(__name__)


class ContentModel(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[ImageOut] = None


class MessageModel(BaseModel):
    role: str = "user"
    content: List[ContentModel]


class PayLoadModel(BaseModel):
    model: str = "gpt-4-vision-preview"
    messages: List[MessageModel]
    temperature: int = 0
    max_tokens: int = 300


class MessageResponse(BaseModel):
    role: str
    content: str


class ResponseChoices(BaseModel):
    message: MessageResponse
    finish_reason: str
    index: int


class OpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: dict
    choices: List[ResponseChoices]


class OpenAiClient(BaseModel):
    api_key: str = settings.OPEN_AI_KEY

    def make_request(self, payload: PayLoadModel):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload_json = payload.model_dump(exclude_none=True)

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload_json,
        )

        if response.status_code == 200:
            return OpenAIResponse.model_validate(response.json())
        else:
            return "Error"


def get_openai_client() -> Generator:
    session = OpenAiClient()
    yield session
