# Vibe Fashion - Streamlit Quick Start

Get the Vibe Fashion Streamlit app running in minutes!

## 🚀 Quick Start (3 steps)

### 1. Setup Environment
```bash
python setup_environment.py
```

### 2. Start the Application
```bash
python start_app.py
```

### 3. Open Your Browser
- Frontend: http://localhost:8501
- Backend: http://localhost:8000

That's it! 🎉

## 📱 What You'll Get

- **Upload Images**: Take or upload photos of yourself
- **AI Fashion Advice**: Get personalized outfit suggestions
- **Generated Outfits**: See AI-generated outfit images
- **Modern Interface**: Clean, responsive Streamlit UI

## 🔧 Manual Setup (if needed)

If the quick start doesn't work, try manual setup:

### Backend Only
```bash
cd services/backend
uv run python main.py
```

### Frontend Only
```bash
python run_streamlit.py
```

### Full App (both backend + frontend)
```bash
python run_full_app.py
```

## 🛠️ Troubleshooting

### Backend Won't Start
- Make sure you have `uv` installed: `pip install uv`
- Check if port 8000 is available
- Run `cd services/backend && uv sync` to install dependencies

### Frontend Won't Start
- Make sure you have Streamlit: `pip install streamlit`
- Check if port 8501 is available
- Try `streamlit run streamlit_app.py` directly

### No Images Generated
- The app works with placeholder images by default
- For real AI image generation, you need Google API keys
- Edit `services/backend/.env` and add your `GOOGLE_API` key

### Connection Issues
- Make sure both backend and frontend are running
- Check the backend URL in the Streamlit sidebar
- Backend should be at `http://localhost:8000`

## 🎯 Features

### With API Keys (Full Experience)
- Real AI-powered outfit generation
- Google Gemini image editing
- Ollama LLM for fashion advice

### Without API Keys (Demo Mode)
- Placeholder outfit images
- Basic fashion suggestions
- Full UI experience

## 📁 File Structure

```
vibe-fashion/
├── start_app.py              # 🚀 Main startup script
├── setup_environment.py      # 🔧 Environment setup
├── run_full_app.py          # 🔄 Full app runner
├── streamlit_app.py         # 📱 Streamlit frontend
├── run_streamlit.py         # 🎯 Streamlit runner
└── services/backend/        # 🔧 FastAPI backend
    ├── main.py
    ├── api.py
    └── core/
        ├── fashion_workflow.py           # Main AI workflow
        └── fashion_workflow_fallback.py  # Fallback for demo
```

## 💡 Tips

- **First time?** Use `python start_app.py` - it handles everything
- **Having issues?** Check the troubleshooting section above
- **Want real AI?** Get Google API keys and add them to `.env`
- **Just testing?** The app works great with placeholder images

## 🆘 Need Help?

1. **Check the logs** - Look for error messages in the terminal
2. **Verify ports** - Make sure 8000 and 8501 are available
3. **Test backend** - Visit http://localhost:8000 to see if it's running
4. **Test frontend** - Visit http://localhost:8501 to see the UI

The app is designed to work even without API keys, so you can test the full experience with placeholder images!
