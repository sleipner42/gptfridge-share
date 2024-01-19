from datetime import datetime, timezone
from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

Data = TypeVar("Data")


class BaseResponse(BaseModel, Generic[Data]):
    """
    Standard response class that should be returned by all endpoints by default.
    """

    data: Optional[Union[Data, List[Data]]]

    class Config:
        validate_assignment = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat(),
        }
