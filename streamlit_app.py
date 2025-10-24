import streamlit as st
import requests
import base64
import io
import os
from PIL import Image
import json

# Configure the page
st.set_page_config(
    page_title="Vibe Fashion - AI Fashion Assistant",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #A23B72;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .image-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        margin: 1rem 0;
    }
    .outfit-image {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 0.5rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">👗 Vibe Fashion</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Fashion Assistant</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Backend URL configuration
    backend_url = st.text_input(
        "Backend URL",
        value=os.getenv("BACKEND_URL", "http://localhost:8000"),
        help="URL of your FastAPI backend server (e.g., https://your-app.railway.app)"
    )
    
    # API endpoint
    api_endpoint = f"{backend_url}/fashion-workflow"
    
    st.markdown("---")
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload an image** of yourself or a person
    2. **Enter your fashion request** (e.g., "casual outfit for work")
    3. **Click 'Get Fashion Suggestions'** to generate outfit recommendations
    4. **View the results** with AI-generated outfit images
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Upload Image")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload a clear image of yourself or the person you want to style"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        st.success("✅ Image uploaded successfully!")
    else:
        img_base64 = None
        st.info("Please upload an image to get started")

with col2:
    st.header("💬 Fashion Request")
    
    # User input
    user_input = st.text_area(
        "Describe what kind of outfit you're looking for:",
        placeholder="e.g., 'casual outfit for a coffee date', 'professional look for an interview', 'summer vacation style'",
        height=100,
        help="Be specific about the occasion, style, or preferences"
    )
    
    # Submit button
    if st.button("🎯 Get Fashion Suggestions", type="primary", disabled=img_base64 is None or not user_input.strip()):
        if img_base64 and user_input.strip():
            with st.spinner("🤖 AI is analyzing your image and generating fashion suggestions..."):
                try:
                    # Prepare the request
                    payload = {
                        "base64_image": img_base64,
                        "user_input": user_input.strip()
                    }
                    
                    # Make the API call
                    response = requests.post(api_endpoint, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("success", False):
                            # Display success message
                            st.markdown('<div class="success-box">✅ Fashion suggestions generated successfully!</div>', unsafe_allow_html=True)
                            
                            # Display text suggestions
                            st.header("💡 Fashion Suggestions")
                            st.write(result.get("text", "No suggestions available"))
                            
                            # Display generated images
                            images = result.get("images", [])
                            if images:
                                st.header("🎨 Generated Outfit Images")
                                
                                # Create columns for images
                                num_images = len(images)
                                if num_images <= 2:
                                    cols = st.columns(num_images)
                                else:
                                    cols = st.columns(2)
                                
                                for i, img_data in enumerate(images):
                                    if i < len(cols):
                                        with cols[i % 2]:
                                            try:
                                                # Decode base64 image
                                                img_bytes = base64.b64decode(img_data.get("base64", ""))
                                                img = Image.open(io.BytesIO(img_bytes))
                                                
                                                st.image(
                                                    img,
                                                    caption=img_data.get("description", f"Outfit {i+1}"),
                                                    use_column_width=True
                                                )
                                            except Exception as e:
                                                st.error(f"Error displaying image {i+1}: {str(e)}")
                            else:
                                st.warning("No outfit images were generated")
                        else:
                            # Display error message
                            error_msg = result.get("error_message", "Unknown error occurred")
                            st.markdown(f'<div class="error-box">❌ Error: {error_msg}</div>', unsafe_allow_html=True)
                    
                    else:
                        st.error(f"API request failed with status code: {response.status_code}")
                        try:
                            error_detail = response.json()
                            st.error(f"Error details: {error_detail}")
                        except:
                            st.error(f"Response: {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to the backend server. Please check if the server is running and the URL is correct.")
                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. The AI processing is taking longer than expected.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
        else:
            st.warning("⚠️ Please upload an image and enter your fashion request")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>Powered by AI • Built with Streamlit • Vibe Fashion</p>
    </div>
    """,
    unsafe_allow_html=True
)
