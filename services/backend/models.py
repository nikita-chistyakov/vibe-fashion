from pydantic import BaseModel
from typing import Optional, List


class ImageResponse(BaseModel):
    """Model for individual image in response"""

    base64: str
    description: str


class FashionResponse(BaseModel):
    """Response model for fashion endpoint"""

    text: str
    images: List[ImageResponse]
    success: bool = True
    error_message: Optional[str] = None
