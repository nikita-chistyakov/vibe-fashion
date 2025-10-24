# Vibe Fashion - Streamlit Frontend Setup

This guide will help you set up and run the Vibe Fashion application with a Streamlit frontend.

## 🚀 Quick Start

### 1. Setup Dependencies
```bash
# Run the setup script
python setup_streamlit.py
```

Or manually install dependencies:
```bash
# Using uv (recommended)
uv add streamlit requests pillow

# Or using pip
pip install -r requirements.txt
```

### 2. Start the Backend
```bash
cd services/backend
python main.py
```
The backend will be available at `http://localhost:8000`

### 3. Start the Streamlit Frontend
```bash
# From the project root
python run_streamlit.py
```
The frontend will be available at `http://localhost:8501`

## 📱 Features

The Streamlit frontend provides:

- **Image Upload**: Upload photos of yourself or others
- **Fashion Requests**: Describe what kind of outfit you want
- **AI Suggestions**: Get personalized fashion recommendations
- **Generated Outfits**: View AI-generated outfit images
- **Responsive Design**: Clean, modern interface

## 🔧 Configuration

### Backend URL
You can configure the backend URL in the Streamlit sidebar. Default is `http://localhost:8000`.

### Environment Variables
Make sure your backend has the necessary environment variables set up (see the backend README).

## 🎯 Usage

1. **Upload an Image**: Choose a clear photo of yourself or the person you want to style
2. **Enter Your Request**: Describe the occasion, style, or preferences
3. **Get Suggestions**: Click "Get Fashion Suggestions" to generate recommendations
4. **View Results**: See AI-generated outfit images and text suggestions

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure the backend is running on the correct port
- Check the backend URL in the Streamlit sidebar
- Verify the backend API is accessible

### Image Upload Issues
- Use supported formats: PNG, JPG, JPEG, WEBP
- Ensure images are clear and well-lit
- Try smaller image sizes if processing is slow

### Dependencies Issues
- Make sure you're using Python 3.11+
- Try reinstalling dependencies: `pip install -r requirements.txt`
- Check for version conflicts

## 📁 File Structure

```
vibe-fashion/
├── streamlit_app.py          # Main Streamlit application
├── run_streamlit.py          # Streamlit runner script
├── setup_streamlit.py        # Setup script
├── requirements.txt           # Python dependencies
├── STREAMLIT_SETUP.md        # This file
└── services/backend/         # FastAPI backend
    ├── api.py
    ├── main.py
    └── ...
```

## 🔄 Development

### Running in Development Mode
```bash
# Backend with auto-reload
cd services/backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Streamlit with auto-reload
streamlit run streamlit_app.py --server.port 8501
```

### Customizing the Frontend
- Edit `streamlit_app.py` to modify the UI
- Update CSS in the `st.markdown()` sections
- Add new features by extending the API calls

## 📊 API Integration

The Streamlit app communicates with the FastAPI backend via:

- **Endpoint**: `POST /fashion-workflow`
- **Request**: `{"base64_image": "...", "user_input": "..."}`
- **Response**: `{"text": "...", "images": [...], "success": true}`

## 🚀 Deployment

### Local Development
1. Start backend: `cd services/backend && python main.py`
2. Start frontend: `python run_streamlit.py`
3. Open browser to `http://localhost:8501`

### Production Deployment
- Deploy backend to your preferred platform (Railway, Render, etc.)
- Update the backend URL in Streamlit
- Deploy Streamlit using Streamlit Cloud or similar service

## 💡 Tips

- Use high-quality, well-lit images for best results
- Be specific in your fashion requests
- The AI works better with clear descriptions of occasions
- Try different image angles and styles for varied results
