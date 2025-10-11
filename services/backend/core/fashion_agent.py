# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pathlib import Path
from typing import Dict, Any, List
import base64
from io import BytesIO

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.cloud import logging as google_cloud_logging
import google.auth
from PIL import Image

# Load environment variables
root_dir = Path(__file__).parent.parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Use default project from credentials if not in .env
try:
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
except Exception:
    pass

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "europe-west1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Set up Cloud Logging
logging_client = google_cloud_logging.Client()
logger = logging_client.logger("fashion-agent")


class FashionAgent:
    """Simple fashion agent for image + text processing"""

    def __init__(self):
        # Configure the model
        gemma_model_name = os.getenv("GEMMA_MODEL_NAME", "gemma3:12b")
        api_base = os.getenv(
            "OLLAMA_API_BASE", "https://ollama-153939933605.europe-west1.run.app"
        )

        self.agent = Agent(
            model=LiteLlm(model=f"ollama_chat/{gemma_model_name}", api_base=api_base),
            name="fashion_agent",
            description="Fashion consultant for image and text analysis",
            instruction="""You are 'Vibe', a fashion consultant. Analyze the provided image and text to give fashion advice, styling tips, and outfit recommendations. Be helpful and encouraging.""",
            tools=[],
        )

    async def process_chat(self, text: str, image_data: bytes) -> Dict[str, Any]:
        """Process chat with image and text input"""
        try:
            # Convert image to base64 for the agent
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            # Create prompt with image context
            prompt = f"User message: {text}\n\nPlease analyze the provided image and give fashion advice."

            # Get response from agent
            response = await self.agent.run(prompt)

            # Generate sample fashion images as base64
            sample_images = self._generate_sample_images(text)

            return {"text": str(response), "images": sample_images, "success": True}

        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return {
                "text": "I'm sorry, I encountered an error. Please try again.",
                "images": [],
                "success": False,
                "error": str(e),
            }

    def _generate_sample_images(self, text: str) -> List[Dict[str, str]]:
        """Generate sample fashion images as base64"""
        # Create simple colored squares as sample images
        sample_images = []

        # Generate 3 different colored squares
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        descriptions = ["Casual outfit", "Professional look", "Evening wear"]

        for i, (color, desc) in enumerate(zip(colors, descriptions)):
            # Create a simple colored image
            img = Image.new("RGB", (200, 200), color)

            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            sample_images.append({"base64": img_base64, "description": desc})

        return sample_images


# Global agent instance
fashion_agent = FashionAgent()
