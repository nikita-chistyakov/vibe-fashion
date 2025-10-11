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
import base64
import binascii
import json
import requests
import logging
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# Setup simple logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
root_dir = Path(__file__).parent.parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)


def call_ollama(
    user_prompt: str = None,
    system_prompt: str = None,
    history: list = None,
    model: str = "gemma3:12b",
    stream: bool = False,
) -> str:
    """Simple function to call Ollama API with flexible message handling"""
    try:
        url = "https://ollama-gemma3-4b-153939933605.europe-west1.run.app/api/chat"

        # Build messages array
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add history if provided
        if history:
            messages.extend(history)

        # Add user prompt if provided
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})

        # If no messages, return error
        if not messages:
            return "Error: No messages provided"

        payload = {
            "model": model,
            "messages": messages,
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


def generate_image(base64_image: str, prompt: str) -> str:
    """
    Input:
        base64_image: Base64-encoded image data (string)
        prompt: Text instruction describing how to modify the image

    Output:
        Base64-encoded PNG data (string)
    """

    API_KEY = os.getenv("GOOGLE_API")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "role": "model",
                "parts": [
                    {
                        "text": """You are a precise image-editing assistant. 
        Output only base64 PNG data, no text, no explanations.
        Take the entry of the base64 image I will give you, do not modify the core of the image,
        do not modify anything unless explicitly stated in the user_prompt I will give you."""
                    }
                ],
            },
            {
                "role": "user",
                "parts": [
                    {"text": f"Here are the intructions: {prompt}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                ],
            },
        ]
    }

    try:
        response = requests.post(
            url, headers={"Content-Type": "application/json"}, data=json.dumps(payload)
        )
        response_data = response.json()
        parts = response_data["candidates"][0]["content"]["parts"]

        for part in parts:
            if "inlineData" in part:
                b64_output = part["inlineData"]["data"]
                try:
                    base64.b64decode(b64_output, validate=True)
                    return b64_output
                except binascii.Error:
                    print("Invalid base64 data detected.")

    except Exception as e:
        print(f"Unexpected error: {e}")


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

            intent_response = call_ollama(user_prompt=intent_prompt)
            intent_classification = str(intent_response).strip().upper()
            logger.info(f"Intent Classification: {intent_classification}")

            if intent_classification == "OUT_OF_TOPIC":
                out_of_topic_response = f""" OUT OF TOPIC: I specialize in providing outfit suggestions with generated visual examples."""
                return {
                    "suggestions": out_of_topic_response,
                    "success": True,
                    "intent_classification": intent_classification,
                    "generated_images": [],
                }
            if intent_classification == "FASHION_REQUEST":
                # call gemma model to generate a set of prompt ( for example 2 )
                # we will call the image_generator tool twice to generate 2 images
                # we will return the images and the prompts
                # Step 3a: Generate two outfit prompts using Gemma
                generation_prompt = f"""
                The user provided this fashion-related request:
                "{user_input}"

                Analyze the user's preferences and generate 2 diverse, creative outfit ideas.
                Each idea should be a one-sentence visual description that can be used as an image-generation prompt.
                
                Example output format (strictly JSON):
                {{
                    "outfits": [
                        "Prompt 1: A modern casual outfit with a denim jacket and white sneakers.",
                        "Prompt 2: A chic summer dress with floral prints and sun hat."
                    ]
                }}
                """

                generation_response = call_ollama(user_prompt=generation_prompt)
                logger.info(f"Outfit Generation Raw Response: {generation_response}")

                try:
                    outfit_data = json.loads(generation_response)
                    outfit_prompts = outfit_data.get("outfits", [])
                except json.JSONDecodeError:
                    # fallback if Gemma didn't return strict JSON
                    outfit_prompts = [
                        line.strip()
                        for line in generation_response.split("\n")
                        if line.strip()
                    ][:2]

                # Step 3b: Generate images using Gemini image model
                generated_images = []
                for prompt in outfit_prompts[:2]:
                    logger.info(f"Generating image for prompt: {prompt}")
                    img_b64 = generate_image(base64_image, prompt)
                    if img_b64:
                        generated_images.append(
                            {"prompt": prompt, "image_base64": img_b64}
                        )

                # Step 3c: Return results
                return {
                    "suggestions": outfit_prompts,
                    "success": True,
                    "intent_classification": intent_classification,
                    "generated_images": generated_images,
                }

            else:
                return {
                    "suggestions": "Intent classification is not valid",
                    "success": False,
                    "error": "Invalid intent classification",
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
