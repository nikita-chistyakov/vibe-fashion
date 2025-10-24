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
import concurrent.futures
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# Setup simple logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def call_ollama(
    user_prompt: str = None,
    system_prompt: str = None,
    history: list = None,
    model: str = "gemma3:12b",
    base64_image: str = None,
    stream: bool = False,
    json_mode: bool = False,
) -> str:
    """
    Calls an Ollama model (multimodal & JSON-safe).
    Supports system + user prompts, chat history, and optional image input.
    """

    try:
        # Use the correct Ollama API base from settings
        from settings import OLLAMA_API_BASE
        url = f"{OLLAMA_API_BASE}/api/chat"

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if history:
            messages.extend(history)

        if user_prompt:
            user_message = {"role": "user", "content": user_prompt}
            if base64_image:
                user_message["images"] = [base64_image]
            messages.append(user_message)

        if not messages:
            return "Error: No messages provided"

        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

        if json_mode:
            payload["format"] = "json"

        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()

        # Return the actual content
        data = response.json()
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        elif "content" in data:
            return data["content"]
        else:
            return json.dumps(data)

    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        return f"Error: {str(e)}"


def generate_image(base64_image: str, prompt: str) -> str:
    """
    Input:
        base64_image: Base64-encoded image data (string)
        prompt: Text instruction describing how to modify the image

    Args:
        base64_image: Base64-encoded image data
        prompt: Text describing how to modify the image

    Returns:
        Base64-encoded PNG data
    """
    print(f"Generating image for prompt: {prompt}")
    API_KEY = os.getenv("GOOGLE_API")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "role": "model",
                "parts": [
                    {
                        "text": """You are a precise image-editing assistant.

                        GOAL
                        - Edit ONLY the clothing on the person in the provided image per the user's instruction.
                        - Preserve identity: do not change face, skin tone, hair, body shape, age, pose, lighting, or background.

                        OUTPUT
                        - Return a base64-encoded PNG ONLY (no JSON, no text, no markdown, no prefix/suffix).

                        CONSTRAINTS
                        - Do not add text, logos, watermarks, or brand marks.
                        - Do not sexualize or remove garments.
                        - If instruction conflicts with identity preservation, favor preservation and still return the best clothing-only edit.
                        """
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
    """Fashion workflow that classifies user intent and generates outfit suggestions"""

    def __init__(self):
        pass

    async def process_request(
        self, base64_image: str, user_input: str
    ) -> Dict[str, Any]:
        """Process fashion request with intent classification and conditional outfit generation"""
        print(f"Processing request: {user_input[:50]}...")

        try:
            # Step 1: Intent Classification
            print("Classifying intent...")
            intent_prompt = f"""
            Figure out what the user is asking for.

            Return EXACTLY one label on a single line with no punctuation or quotes:
            FASHION_REQUEST or OUT_OF_TOPIC

            Guidelines:
            - FASHION_REQUEST = outfits, clothing styling, wardrobe advice, or garment changes to the person in the image.
            - OUT_OF_TOPIC = makeup/hair/face/body edits, background-only edits, or unrelated/unclear text.
            - If uncertain, choose OUT_OF_TOPIC.

            Image provided: YES

            Few-shot examples:
            Q: "Make two streetwear looks I could wear with this pic"
            A: FASHION_REQUEST
            Q: "Can you whiten my teeth?"
            A: OUT_OF_TOPIC
            Q: "Put me on a beach"
            A: OUT_OF_TOPIC
            Q: "Suggest smart-casual outfits for the office"
            A: FASHION_REQUEST

            User input:
            <<<{user_input}>>>
            """

            intent_response = call_ollama(
                user_prompt=intent_prompt,
                base64_image=base64_image,  # Send the image for context
            )
            intent_classification = str(intent_response).strip().upper()
            print(f"Intent: {intent_classification}")

            # Handle API failures gracefully
            if "Error:" in intent_classification or "error" in intent_classification.lower():
                print("Ollama API failed, defaulting to FASHION_REQUEST")
                intent_classification = "FASHION_REQUEST"

            if intent_classification == "OUT_OF_TOPIC":
                print("Out of topic - returning redirect message")
                out_of_topic_response = call_ollama(
                    user_prompt=f"""
                You are a fashion assistant, the user ask something that is not related to outfit generation or is unclear
                ask for some clarification and say that you are only here to help with outfit generation.
                User input: {user_input}
                """,
                )
                return {
                    "suggestions": out_of_topic_response,
                    "success": True,
                    "intent_classification": intent_classification,
                    "generated_images": [],
                }
            if intent_classification == "FASHION_REQUEST":
                print("Fashion request - generating outfits...")
                # call gemma model to generate a set of prompt ( for example 2 )
                # we will call the image_generator tool twice to generate 2 images
                # we will return the images and the prompts
                # Step 3a: Generate two outfit prompts using Gemma
                print("Generating outfit prompts...")
                generation_prompt = f"""
                You are generating two outfit-edit prompts for an image editor.

                REQUIRED OUTPUT FORMAT (exactly this shape):
                {{
                "outfits": [
                    "string",
                    "string",
                    "string",
                    "string"
                ]
                }}

                Rules:
                - Return VALID JSON only. No markdown, no comments, no extra keys, no trailing commas.
                - The "outfits" array must contain EXACTLY 4 strings.

                CONTENT RULES FOR EACH STRING:
                - Start with: "Replace current clothing with ..."
                - ≤ 60 words.
                - Mention silhouette, a 3–5 color palette, main garments, fabric/texture, footwear, and 1–2 accessories.
                - Include this clause verbatim: "keep body, face, hair, skin tone, pose, lighting, and background unchanged."
                - No brand names, no text overlays, no camera/aspect settings.
                - If the user gives no setting, assume a neutral studio background.
                - Write in the same language as the User Input.

                FEW-SHOT EXAMPLES (follow these patterns exactly):

                Example 1:
                {{
                "outfits": [
                    "Replace current clothing with a sleek streetwear look — oversized black hoodie, gray joggers, and chunky white sneakers; add a silver chain. keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                    "Replace current clothing with a modern minimalist outfit — white cropped shirt, high-waisted beige trousers, and brown loafers with a thin leather belt; subtle gold jewelry. keep body, face, hair, skin tone, pose, lighting, and background unchanged."
                ]
                }}

                Example 2:
                {{
                "outfits": [
                    "Replace current clothing with a relaxed summer outfit — light blue linen shirt, white shorts, tan sandals, and a woven bracelet; breezy, casual vibe. keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                    "Replace current clothing with an elegant evening style — satin black dress, silver heels, and minimalist pearl earrings; add soft fabric sheen. keep body, face, hair, skin tone, pose, lighting, and background unchanged."
                ]
                }}

                User Input:
                \"\"\"{user_input}\"\"\"
                """

                generation_response = call_ollama(
                    user_prompt=generation_prompt,
                    json_mode=True,  # Force strict JSON output
                )
                print("Generated prompts")

                try:
                    outfit_data = json.loads(generation_response)
                    outfit_prompts = outfit_data.get("outfits", [])
                except json.JSONDecodeError:
                    # fallback if Gemma didn't return strict JSON
                    outfit_prompts = [
                        line.strip()
                        for line in generation_response.split("\n")
                        if line.strip()
                    ][:4]
                
                # If API failed, use default prompts
                if not outfit_prompts or "Error:" in str(generation_response):
                    print("Ollama API failed for generation, using default prompts")
                    outfit_prompts = [
                        f"Replace current clothing with a casual outfit based on: {user_input}. keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                        f"Replace current clothing with a professional outfit based on: {user_input}. keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                        f"Replace current clothing with a stylish outfit based on: {user_input}. keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                        f"Replace current clothing with a trendy outfit based on: {user_input}. keep body, face, hair, skin tone, pose, lighting, and background unchanged."
                    ]

                # Step 3b: Generate images using Gemini image model concurrently
                print("Generating images...")
                generated_images = []

                # Use ThreadPoolExecutor for concurrent image generation
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    # Submit image generation tasks
                    future_to_prompt = {
                        executor.submit(generate_image, base64_image, prompt): (
                            i,
                            prompt,
                        )
                        for i, prompt in enumerate(outfit_prompts[:4], 1)
                    }

                    # Collect results as they complete
                    for future in concurrent.futures.as_completed(future_to_prompt):
                        i, prompt = future_to_prompt[future]
                        print(f"  Image {i}/4...")
                        try:
                            img_b64 = future.result()
                            if img_b64:
                                generated_images.append(
                                    {"prompt": prompt, "image_base64": img_b64}
                                )
                                print(f"  Image {i} generated")
                            else:
                                print(f"  Image {i} failed")
                        except Exception as e:
                            print(f"  Image {i} failed with error: {e}")

                print(f"Complete! Generated {len(generated_images)} images")
                # Step 3c: Return results
                # another call to generate combinatining the prompts descriptions , a readable description of the image

                print("Creating combined outfit description...")

                try:
                    system_prompt = (
                        "You are a professional fashion stylist and copywriter. "
                        "You write vivid, elegant, and concise outfit descriptions for clients. "
                        "Focus on tone, mood, and visual coherence — not just listing items."
                    )

                    user_prompt = f"""
                    These outfit ideas were generated for the user:
                    {json.dumps(outfit_prompts, indent=2)}

                    Write a short paragraph (3–5 sentences) that smoothly describes these outfits
                    as if summarizing them for a fashion magazine feature. 
                    Avoid JSON, lists, or code blocks — produce only natural language text.
                    """

                    summary_output = call_ollama(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        model="gemma3:12b",
                    )
                    print("Combined description generated successfully.")

                except Exception as e:
                    print(f"Failed to generate combined description: {e}")
                    summary_output = "No readable description available."
                
                # If API failed, use a simple fallback description
                if "Error:" in str(summary_output) or not summary_output.strip():
                    print("Ollama API failed for summary, using fallback description")
                    summary_output = f"Here are some outfit suggestions based on your request: '{user_input}'. I've generated 4 different outfit variations for you to choose from. Each outfit maintains your personal style while incorporating the elements you requested."

                # Return the summary as 'suggestions'
                return {
                    "suggestions": summary_output,  # now contains the natural-language paragraph
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
            print(f"Error: {str(e)}")
            return {
                "suggestions": "I'm sorry, I encountered an error analyzing your request. Please try again.",
                "success": False,
                "error": str(e),
                "intent_classification": "ERROR",
                "generated_images": [],
            }


# Global workflow instance
fashion_workflow = FashionWorkflow()
