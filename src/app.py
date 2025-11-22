import streamlit as st
from PIL import Image
import os
from utils import calculate_sha256_bytes
from recommend import get_recommendation
from backend import AgriGuardModel
from frontend import (
    apply_custom_css,
    render_hero,
    render_file_uploader,
    render_integrity_badge,
    render_results,
    render_trust_section
)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/agriguard_model.pth')
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '../models/class_indices.json')

# Page Configuration
st.set_page_config(
    page_title="AgriGuard AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_custom_css()

# Initialize model (cached)
@st.cache_resource
def get_model():
    """Load and cache the model"""
    model_handler = AgriGuardModel(MODEL_PATH, CLASS_INDICES_PATH)
    success = model_handler.load_model()
    return model_handler if success else None

# Load model
model_handler = get_model()

# Render hero section
render_hero()

# File upload section
uploaded_file = render_file_uploader()

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, use_container_width=True)
    
    # Show integrity badge
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    file_hash = calculate_sha256_bytes(file_bytes)
    render_integrity_badge(file_hash)
    
    # Check if model is loaded
    if model_handler is None:
        st.error("⚠️ Model not found. Please train the model first using `python train.py`.")
    else:
        # Analyze button
        if st.button("🔍 Analyze Image"):
            with st.spinner('🔬 Analyzing your plant...'):
                try:
                    # Make prediction
                    predicted_class_name, confidence_score = model_handler.predict(image)
                    
                    # Get recommendation
                    advice = get_recommendation(predicted_class_name)
                    
                    # Render results
                    render_results(predicted_class_name, confidence_score, advice)
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

# Footer
render_trust_section()