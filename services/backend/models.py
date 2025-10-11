from pydantic import BaseModel
from typing import List, Optional


class ImageResponse(BaseModel):
    """Model for individual image in response"""

    base64: str
    description: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    text: str
    images: List[ImageResponse]
    success: bool = True
    error_message: Optional[str] = None
