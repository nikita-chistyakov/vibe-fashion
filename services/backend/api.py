from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import uvicorn

from models import ChatResponse, ImageResponse
from core.fashion_agent import fashion_agent
from image_utils import process_uploaded_image, validate_image_format

# Create FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vibe Fashion API is running!", "status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(
    text: str = Form(..., description="User's text message"),
    image: UploadFile = File(..., description="Image file"),
):
    """
    Simple chat endpoint that requires both text and image input

    Args:
        text: User's text message
        image: Required image file

    Returns:
        ChatResponse with AI response text and base64 images
    """
    try:
        # Validate image format
        image_content = await image.read()
        if not validate_image_format(image_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid image format. Please upload a valid image file.",
            )

        # Process the image
        processed_image = process_uploaded_image(image_content)
        if not processed_image:
            raise HTTPException(
                status_code=400, detail="Failed to process the uploaded image."
            )

        # Get response from the fashion agent
        response = await fashion_agent.process_chat(text, processed_image)

        # Convert images to the expected format
        images = [
            ImageResponse(base64=img["base64"], description=img["description"])
            for img in response["images"]
        ]

        return ChatResponse(
            text=response["text"],
            images=images,
            success=response["success"],
            error_message=response.get("error"),
        )

    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            text="I'm sorry, I encountered an error processing your request.",
            images=[],
            success=False,
            error_message=str(e),
        )


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
