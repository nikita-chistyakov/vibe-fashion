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
import json
import requests
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# Load environment variables
root_dir = Path(__file__).parent.parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)


def call_ollama(prompt: str, model: str = "gemma3:12b", stream: bool = False) -> str:
    """Simple function to call Ollama API"""
    try:
        url = "https://ollama-gemma3-4b-153939933605.europe-west1.run.app/api/chat"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream,
        }

        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        if stream:
            # Handle streaming response
            result = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "message" in data and "content" in data["message"]:
                            result += data["message"]["content"]
                    except json.JSONDecodeError:
                        continue
            return result
        else:
            # Handle non-streaming response
            data = response.json()
            return data.get("message", {}).get("content", "")

    except Exception as e:
        print(f"Error calling Ollama: {str(e)}")
        return f"Error: {str(e)}"


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


class FashionWorkflow:
    """Enhanced fashion workflow with intent classification and conditional outfit generation"""

    def __init__(self):
        pass

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

            intent_response = call_ollama(intent_prompt)
            intent_classification = str(intent_response).strip().upper()

            # Step 2: Conditional Processing
            if intent_classification == "FASHION_REQUEST":
                # Proceed with outfit generation
                outfit_prompt = f"""Generate outfit suggestions based on the user's request.

                User Input: {user_input}
                Image Data: {base64_image}
                
                Provide 4 different outfit suggestions with detailed descriptions and generate images for each."""

                outfit_response = call_ollama(outfit_prompt)

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
