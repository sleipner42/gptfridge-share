import base64
import io
from typing import Self

from app.core.logger import get_logger
from PIL import Image
from pydantic import BaseModel

logger = get_logger(__name__)


class ImageIn(BaseModel):
    image: str
    name: str

    class Config:
        validate_assignment = True


class ImageDTO(BaseModel):
    image_data: str

    class Config:
        validate_assignment = True

    def from_image_in(image_in: ImageIn):
        return ImageDTO(image_data=image_in.image)


class ImageOut(BaseModel):
    url: str

    def from_dto(image: ImageDTO) -> Self:
        image = Image.open(io.BytesIO(base64.b64decode(image.image_data)))
        longest_side = 500
        aspect_ratio = min(longest_side / image.width, longest_side / image.height)
        new_size = (int(image.width * aspect_ratio), int(image.height * aspect_ratio))

        image = image.resize(new_size)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode()

        return ImageOut(url=f"data:image/jpeg;base64,{base64_image}")
