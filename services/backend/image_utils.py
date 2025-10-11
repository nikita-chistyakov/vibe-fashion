from typing import Optional, Tuple
from PIL import Image
import io
import base64


def process_uploaded_image(
    image_data: bytes, max_size: Tuple[int, int] = (1024, 1024)
) -> Optional[bytes]:
    """
    Process uploaded image data

    Args:
        image_data: Raw image bytes
        max_size: Maximum dimensions (width, height)

    Returns:
        Processed image bytes or None if processing fails
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize if too large
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save to bytes
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=85)
        return output.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def image_to_base64(image_data: bytes) -> str:
    """
    Convert image bytes to base64 string

    Args:
        image_data: Image bytes

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(image_data).decode("utf-8")


def base64_to_image(base64_string: str) -> Optional[bytes]:
    """
    Convert base64 string to image bytes

    Args:
        base64_string: Base64 encoded image

    Returns:
        Image bytes or None if conversion fails
    """
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        print(f"Error decoding base64 image: {e}")
        return None


def validate_image_format(image_data: bytes) -> bool:
    """
    Validate if the uploaded data is a valid image

    Args:
        image_data: Raw image bytes

    Returns:
        True if valid image, False otherwise
    """
    try:
        Image.open(io.BytesIO(image_data))
        return True
    except Exception:
        return False


def get_image_info(image_data: bytes) -> Optional[dict]:
    """
    Get basic information about the image

    Args:
        image_data: Raw image bytes

    Returns:
        Dictionary with image info or None if invalid
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        return {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
        }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None
