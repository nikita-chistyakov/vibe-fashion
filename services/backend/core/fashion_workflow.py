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
from typing import Dict, Any

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import google.auth

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


# Tool for generating images (placeholder for nanobanana integration)
def generate_image(base64_image: str, prompt: str) -> Dict[str, Any]:
    """
    Generate an image based on base64 input image and text prompt.
    This is a placeholder for nanobanana integration.

    Args:
        base64_image: Base64 encoded input image
        prompt: Text prompt for image generation

    Returns:
        Dict containing generated image data and metadata
    """
    # TODO: Integrate with nanobanana API
    # For now, return a placeholder response
    return {
        "success": True,
        "generated_image": base64_image,  # Placeholder - would be new generated image
        "prompt_used": prompt,
        "metadata": {"model": "nanobanana_placeholder", "generation_time": "0.5s"},
    }


# Note: Tool integration will be added later when nanobanana API is integrated


class FashionWorkflow:
    """Enhanced fashion workflow with intent classification and conditional outfit generation"""

    def __init__(self):
        # Configure the model
        gemma_model_name = os.getenv("GEMMA_MODEL_NAME", "gemma3:12b")
        api_base = os.getenv(
            "OLLAMA_API_BASE", "https://ollama-153939933605.europe-west1.run.app"
        )

        # Intent classification agent
        self.intent_classifier = Agent(
            model=LiteLlm(model=f"ollama_chat/{gemma_model_name}", api_base=api_base),
            name="intent_classifier",
            description="Classifies user intent for fashion requests",
            instruction="""You are an intent classifier for fashion requests. 
            
            Your task:
            1. Analyze the user's input and image to determine their intent
            2. Classify if they want outfit suggestions with generated images
            3. Respond with ONLY one of these classifications:
               - "FASHION_REQUEST": User wants outfit suggestions with generated images
               - "OUT_OF_TOPIC": User's request is not related to outfit generation or is unclear
            
            Be conservative - only classify as FASHION_REQUEST if the user clearly wants outfit suggestions.""",
        )

        # Outfit generation agent
        self.outfit_generator = Agent(
            model=LiteLlm(model=f"ollama_chat/{gemma_model_name}", api_base=api_base),
            name="outfit_generator",
            description="Generates outfit suggestions with visual examples",
            instruction="""You are 'Vibe', a fashion consultant specializing in outfit generation. 
            
            Your task:
            1. Provide 4 different outfit suggestions with detailed descriptions
            2. Describe what each outfit would look like visually
            3. Return detailed textual descriptions for each outfit
            
            Each outfit suggestion should include:
            - Style description
            - Key pieces (top, bottom, shoes, accessories)
            - Colors and textures
            - Suitable occasions
            - Why this combination works well
            - Visual description of how the outfit would look
            
            Be specific about clothing items, accessories, colors, and occasions. Be helpful and encouraging.""",
        )

    async def process_request(
        self, base64_image: str, user_input: str
    ) -> Dict[str, Any]:
        """Process fashion request with intent classification and conditional outfit generation"""
        try:
            # Step 1: Intent Classification
            intent_prompt = f"""Analyze the user's request and classify their intent.

            User Input: {user_input}
            Image Data: {base64_image}
            
            Classify the user's intent and respond with ONLY one of these:
            - "FASHION_REQUEST": User wants outfit suggestions with generated images
            - "OUT_OF_TOPIC": User's request is not related to outfit generation or is unclear"""

            intent_response = await self.intent_classifier.run(intent_prompt)
            intent_classification = str(intent_response).strip().upper()

            # Step 2: Conditional Processing
            if intent_classification == "FASHION_REQUEST":
                # Proceed with outfit generation
                outfit_prompt = f"""Generate outfit suggestions based on the user's request.

                User Input: {user_input}
                Image Data: {base64_image}
                
                Provide 4 different outfit suggestions with detailed descriptions and generate images for each."""

                outfit_response = await self.outfit_generator.run(outfit_prompt)

                return {
                    "suggestions": str(outfit_response),
                    "success": True,
                    "intent_classification": intent_classification,
                    "generated_images": [],  # Will be populated by the agent's tool calls
                }

            else:  # OUT_OF_TOPIC or any other classification - treat as out of topic
                out_of_topic_response = f"""I specialize in providing outfit suggestions with generated visual examples. 
                
                Your input: {user_input}
                
                I can help you with specific outfit requests like:
                - "What should I wear to a job interview?"
                - "Help me create a casual weekend outfit"
                - "I need suggestions for a formal event"
                - "What outfit goes with this dress?"
                
                Could you please ask me about a specific outfit or styling request?"""

                return {
                    "suggestions": out_of_topic_response,
                    "success": True,
                    "intent_classification": intent_classification,
                    "generated_images": [],
                }

        except Exception as e:
            print(f"Error processing fashion request: {str(e)}")
            return {
                "suggestions": "I'm sorry, I encountered an error analyzing your request. Please try again.",
                "success": False,
                "error": str(e),
                "intent_classification": "ERROR",
                "generated_images": [],
            }


# Global workflow instance
fashion_workflow = FashionWorkflow()
