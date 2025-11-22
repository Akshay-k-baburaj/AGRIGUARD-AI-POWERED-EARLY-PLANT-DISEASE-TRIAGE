import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import json
import os
from model import build_model
from utils import calculate_sha256_bytes
from recommend import get_recommendation

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/agriguard_model.pth')
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '../models/class_indices.json')

st.set_page_config(page_title="AgriGuard", page_icon="🌿")

st.title("AgriGuard: AI-Powered Plant Disease Detection")
st.write("Upload a leaf image to detect diseases and get agricultural advice.")

@st.cache_resource
def load_trained_model(num_classes):
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = build_model(num_classes)
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval()
        return model, device
    return None, None

@st.cache_data
def load_class_indices():
    if not os.path.exists(CLASS_INDICES_PATH):
        return None
    with open(CLASS_INDICES_PATH, 'r') as f:
        class_indices = json.load(f)
    # Invert: Name -> Index to Index -> Name
    return {v: k for k, v in class_indices.items()}

class_indices = load_class_indices()
if class_indices:
    model, device = load_trained_model(len(class_indices))
else:
    model, device = None, None

uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    # Integrity Check
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    file_hash = calculate_sha256_bytes(file_bytes)
    st.sidebar.success(f"Image Integrity Verified (SHA256): {file_hash[:10]}...")

    if model is None:
        st.error("Model not found. Please train the model first using `src/train.py`.")
    else:
        if st.button("Analyze"):
            with st.spinner('Analyzing...'):
                # Preprocess
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])
                
                input_tensor = transform(image).unsqueeze(0).to(device)

                # Prediction
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probabilities = torch.nn.functional.softmax(outputs, dim=1)
                    confidence, predicted = torch.max(probabilities, 1)
                    
                predicted_class_index = predicted.item()
                predicted_class_name = class_indices[predicted_class_index]
                confidence_score = confidence.item()

                # Display Results
                st.subheader("Result")
                st.write(f"**Prediction:** {predicted_class_name}")
                st.write(f"**Confidence:** {confidence_score:.2%}")

                # Recommendation
                st.subheader("Recommendation")
                advice = get_recommendation(predicted_class_name)
                st.info(advice)
