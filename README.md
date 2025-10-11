# 🎨 Vibe Fashion - AI-Powered Fashion Assistant

> An intelligent fashion companion that analyzes your photos and generates personalized outfit suggestions using advanced AI models.

## 🌟 Overview

Vibe Fashion is a modern web application that combines computer vision and AI to provide personalized fashion advice. Simply capture your image through the webcam, describe what you're looking for, and let our AI generate curated outfit suggestions with visual representations.

## ✨ Features

- **🎥 Real-time Camera Integration**: Capture photos directly through your webcam
- **🤖 AI-Powered Analysis**: Advanced image analysis using state-of-the-art AI models
- **👗 Smart Outfit Generation**: Generate multiple outfit suggestions based on your preferences
- **💬 Natural Language Processing**: Describe your style preferences in natural language
- **🎨 Visual Outfit Recommendations**: Get visual representations of suggested outfits
- **📱 Modern UI**: Clean, responsive design with a beautiful gradient interface

## 🏗️ Architecture

The project follows a microservices architecture with three main components:

```
vibe-fashion/
├── frontend/          # Next.js React application
├── services/
│   ├── backend/      # FastAPI Python backend
│   └── ollama/       # Local AI model server
└── README.md
```

### Frontend (Next.js)
- **Framework**: Next.js 15.5.4 with React 19
- **Styling**: Tailwind CSS with custom gradients
- **State Management**: Zustand for global state
- **UI Components**: Custom components with Radix UI primitives
- **Camera Integration**: Real-time webcam capture and image processing

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11+
- **AI Integration**: Custom fashion workflow with multimodal AI
- **Image Processing**: PIL/Pillow for image manipulation
- **API**: RESTful endpoints with proper CORS handling

### AI Service (Ollama)
- **Model**: Gemma3 (4b/12b variants)
- **Capabilities**: Multimodal understanding (text + images)
- **Local Deployment**: Self-hosted AI model for privacy

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** with `uv` package manager
- **Node.js 18+** with npm
- **Docker** (for containerized deployment)
- **Webcam** (for image capture)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vibe-fashion
   ```

2. **Set up the Backend**
   ```bash
   cd services/backend
   uv sync
   cp .env.example .env  # Configure your environment variables
   ```

3. **Set up the Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Ollama Service**
   ```bash
   cd services/ollama
   docker build -t vibe-fashion-ollama .
   docker run -p 8080:8080 vibe-fashion-ollama
   ```

### Running the Application

1. **Start the Backend**
   ```bash
   cd services/backend
   uv run python main.py
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 🐳 Docker Deployment

Build and run all services using Docker:

```bash
# Build and run the Ollama service
cd services/ollama
docker build -t vibe-fashion-ollama .
docker run -d -p 8080:8080 vibe-fashion-ollama

# Build and run the backend
cd services/backend
docker build -t vibe-fashion-backend .
docker run -d -p 8000:8000 vibe-fashion-backend

# Build and run the frontend
cd frontend
docker build -t vibe-fashion-frontend .
docker run -d -p 3000:3000 vibe-fashion-frontend
```

## 📖 API Documentation

### Fashion Workflow Endpoint

**POST** `/fashion-workflow`

Analyzes an image and user input to generate fashion recommendations.

**Request Body:**
```json
{
  "base64_image": "base64-encoded-image-string",
  "user_input": "Describe what you're looking for..."
}
```

**Response:**
```json
{
  "text": "Fashion suggestions in natural language",
  "images": [
    {
      "base64": "base64-encoded-outfit-image",
      "description": "Outfit description"
    }
  ],
  "success": true,
  "error_message": null
}
```

## 🛠️ Tech Stack

### Frontend
- **Next.js 15.5.4** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **React Hook Form** - Form handling

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **PIL/Pillow** - Image processing
- **python-dotenv** - Environment management

### AI/ML
- **Ollama** - Local AI model serving
- **Gemma3** - Google's AI model
- **LiteLLM** - LLM integration library

## 🎯 How It Works

1. **Image Capture**: User captures or uploads an image through the web interface
2. **Intent Analysis**: AI analyzes the user's text input to understand fashion preferences
3. **Image Analysis**: Computer vision processes the uploaded image
4. **Outfit Generation**: AI generates multiple outfit suggestions based on analysis
5. **Visual Creation**: System creates visual representations of suggested outfits
6. **Response**: User receives both textual descriptions and visual outfit images

## 🔧 Development

### Project Structure

```
frontend/src/
├── app/              # Next.js app router
├── components/       # React components
│   ├── ui/          # Reusable UI components
│   ├── camera.tsx   # Camera integration
│   ├── conversation.tsx  # Chat interface
│   └── ...
├── libs/            # Utilities and stores
│   └── zustand/     # State management
└── utils/           # Helper functions

services/backend/
├── core/            # Core business logic
│   └── fashion_workflow.py  # Main AI workflow
├── api.py          # FastAPI routes
├── models.py       # Pydantic models
└── main.py         # Application entry point
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
OLLAMA_BASE_URL=http://localhost:8080
# Add other configuration as needed
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google** for the Gemma3 AI model
- **Ollama** for local AI model serving
- **Next.js** and **FastAPI** communities for excellent frameworks
- **Tailwind CSS** for beautiful styling utilities

---

**Built with ❤️ for fashion enthusiasts and AI lovers**