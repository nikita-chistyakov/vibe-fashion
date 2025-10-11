# Vibe Fashion API

Simple AI-powered fashion consultation API that requires both image and text input.

## Features

- **Image + Text chat**: Upload images with text for personalized fashion advice
- **Base64 image output**: Returns generated fashion images as base64 strings
- **AI-powered responses**: Powered by Google ADK with Gemma model via Ollama
- **Simple API**: Single endpoint that always requires both image and text

## API Endpoints

### Health Check
- `GET /` - Basic health check

### Chat Endpoint
- `POST /chat` - Chat with required image upload and text input

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure environment**:
   Create a `.env` file with the following variables:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=europe-west1
   OLLAMA_API_BASE=http://localhost:10010
   GEMMA_MODEL_NAME=gemma3:4b
   ```

3. **Start the server**:
   ```bash
   python start_server.py
   ```

   Or directly:
   ```bash
   python api.py
   ```

## Usage Examples

### Chat with Image (Required)
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "text=I need help styling this outfit" \
  -F "image=@your_image.jpg"
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

## API Response Format

The chat endpoint returns:
```json
{
  "text": "AI response text",
  "images": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "description": "Image description"
    }
  ],
  "success": true,
  "error_message": null
}
```

## Requirements

- Python 3.11+
- Ollama server running with Gemma model
- Google Cloud credentials (for production)
- FastAPI and related dependencies (installed via uv)
