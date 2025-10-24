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
import json
import logging
from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io
import random

# Setup simple logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_fashion_placeholder_images(prompts):
    """Create fashion-themed placeholder images when APIs are not available"""
    placeholder_images = []
    
    # Fashion color palettes
    color_palettes = [
        ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],  # Warm tones
        ['#A8E6CF', '#FFD3A5', '#FFAAA5', '#FF8B94'],  # Pastel
        ['#2C3E50', '#34495E', '#E74C3C', '#F39C12'],  # Bold
        ['#8E44AD', '#9B59B6', '#3498DB', '#1ABC9C'],  # Vibrant
    ]
    
    for i, prompt in enumerate(prompts, 1):
        try:
            # Create a fashion-themed placeholder image
            img = Image.new('RGB', (400, 600), color='white')
            draw = ImageDraw.Draw(img)
            
            # Choose a random color palette
            palette = random.choice(color_palettes)
            bg_color = palette[0]
            
            # Create a gradient-like background
            for y in range(600):
                color_intensity = int(255 * (1 - y / 600))
                color = tuple(int(c.replace('#', ''), 16) for c in [bg_color])
                draw.line([(0, y), (400, y)], fill=color)
            
            # Try to use a default font, fallback to basic if not available
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Add fashion-themed text
            title = f"Outfit {i}"
            description = prompt[:80] + "..." if len(prompt) > 80 else prompt
            
            # Draw title
            draw.text((20, 50), title, fill='black', font=font_large)
            
            # Draw description with word wrapping
            words = description.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font_small)
                if bbox[2] - bbox[0] > 360:  # If line is too long
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw lines
            y_pos = 100
            for line in lines[:4]:  # Limit to 4 lines
                draw.text((20, y_pos), line, fill='black', font=font_small)
                y_pos += 25
            
            # Add a simple fashion icon (rectangle representing clothing)
            draw.rectangle([150, 250, 250, 400], outline='black', width=2)
            draw.rectangle([160, 260, 240, 390], fill=palette[1])
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            placeholder_images.append({
                "prompt": prompt,
                "image_base64": img_base64,
                "description": f"Fashion suggestion {i}"
            })
            
        except Exception as e:
            print(f"Failed to create fashion placeholder image {i}: {e}")
            # Create a simple colored rectangle as fallback
            img = Image.new('RGB', (400, 600), color=random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            placeholder_images.append({
                "prompt": prompt,
                "image_base64": img_base64,
                "description": f"Fashion suggestion {i}"
            })
    
    return placeholder_images


class FashionWorkflowFallback:
    """Fallback fashion workflow that works without external APIs"""

    def __init__(self):
        pass

    async def process_request(
        self, base64_image: str, user_input: str
    ) -> Dict[str, Any]:
        """Process fashion request using fallback methods"""
        print(f"Processing request with fallback: {user_input[:50]}...")

        try:
            # Simple intent classification based on keywords
            fashion_keywords = [
                'outfit', 'clothing', 'dress', 'shirt', 'pants', 'style', 'fashion',
                'casual', 'formal', 'professional', 'party', 'work', 'date', 'vacation',
                'summer', 'winter', 'spring', 'fall', 'color', 'accessories'
            ]
            
            user_input_lower = user_input.lower()
            is_fashion_request = any(keyword in user_input_lower for keyword in fashion_keywords)
            
            if not is_fashion_request:
                return {
                    "suggestions": "I'm a fashion assistant! I can help you with outfit suggestions, styling advice, and clothing recommendations. Could you tell me more about what kind of outfit you're looking for?",
                    "success": True,
                    "intent_classification": "OUT_OF_TOPIC",
                    "generated_images": [],
                }
            
            # Generate outfit prompts using simple templates
            outfit_templates = [
                f"Replace current clothing with a casual outfit based on: {user_input}. Keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                f"Replace current clothing with a professional outfit based on: {user_input}. Keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                f"Replace current clothing with a stylish outfit based on: {user_input}. Keep body, face, hair, skin tone, pose, lighting, and background unchanged.",
                f"Replace current clothing with a trendy outfit based on: {user_input}. Keep body, face, hair, skin tone, pose, lighting, and background unchanged."
            ]
            
            # Create placeholder images
            placeholder_images = create_fashion_placeholder_images(outfit_templates)
            
            # Generate a simple description
            suggestions = f"""Here are some outfit suggestions based on your request: "{user_input}".

I've prepared 4 different outfit variations for you:
1. **Casual Style** - Perfect for everyday wear
2. **Professional Look** - Great for work or formal occasions  
3. **Stylish Ensemble** - - A fashionable choice for social events
4. **Trendy Outfit** - Following current fashion trends

Each outfit maintains your personal style while incorporating the elements you requested. The suggestions are designed to be versatile and suitable for various occasions.

*Note: This is a demo version. For actual outfit generation with AI, please configure your API keys.*"""

            return {
                "suggestions": suggestions,
                "success": True,
                "intent_classification": "FASHION_REQUEST",
                "generated_images": placeholder_images,
            }

        except Exception as e:
            print(f"Error in fallback workflow: {str(e)}")
            return {
                "suggestions": "I'm sorry, I encountered an error processing your request. Please try again.",
                "success": False,
                "error": str(e),
                "intent_classification": "ERROR",
                "generated_images": [],
            }


# Global fallback workflow instance
fashion_workflow_fallback = FashionWorkflowFallback()
