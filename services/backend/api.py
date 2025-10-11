from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import base64

from models import FashionResponse
from core.fashion_workflow import fashion_workflow


# Request model for fashion workflow
class FashionWorkflowRequest(BaseModel):
    """Request model for fashion workflow"""

    base64_image: str
    user_input: str


# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vibe Fashion API is running!", "status": "healthy"}


@app.post("/fashion-workflow", response_model=FashionResponse)
async def fashion_workflow_endpoint(request: FashionWorkflowRequest):
    """
    Run the complete fashion workflow with image analysis and outfit generation

    Args:
        request: FashionWorkflowRequest containing base64 image and user input

    Returns:
        FashionWorkflowResponse with textual suggestions and 4 generated outfit images
    """
    try:
        # Validate base64 image
        try:
            # Try to decode the base64 to validate it
            base64.b64decode(request.base64_image)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 image format. Please provide a valid base64 encoded image.",
            )

        # Run the fashion workflow
        result = await fashion_workflow.process_request(
            request.base64_image, request.user_input
        )

        # Convert generated images to the expected format
        images = []
        for img_data in result.get("generated_images", []):
            images.append(
                {
                    "base64": img_data.get("image_base64", ""),
                    "description": img_data.get(
                        "description", "Generated outfit image"
                    ),
                }
            )

        return FashionResponse(
            text=result["suggestions"],
            images=images,
            success=result["success"],
            error_message=result.get("error"),
        )

    except HTTPException:
        raise
    except Exception as e:
        return FashionResponse(
            text="I'm sorry, I encountered an error processing your request.",
            images=[],
            success=False,
            error_message=str(e),
        )


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
