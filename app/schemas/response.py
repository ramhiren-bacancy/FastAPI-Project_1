from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    statusCode: int
    message: str
    data: Optional[T]
    success: bool
    timestamp: datetime