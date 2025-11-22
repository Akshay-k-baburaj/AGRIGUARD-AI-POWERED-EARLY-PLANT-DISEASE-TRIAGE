import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import json
import os
import requests
import datetime
import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import json
import os
import requests
import datetime
import time
from model import build_model
from utils import calculate_sha256_bytes
from recommend import get_recommendation

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/agriguard_model.pth')
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '../models/class_indices.json')
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AgriGuard", page_icon="🌿")

# Session State for Auth
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            st.session_state.auth_token = token
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend server. Is it running?")

def register(email, username, password, full_name, farm_location):
    try:
        payload = {
            "email": email,
            "username": username,
            "password": password,
            "full_name": full_name,
            "farm_location": farm_location
        }
        response = requests.post(f"{API_URL}/auth/register", json=payload)
        if response.status_code == 200:
            st.success("Registration successful! Please login.")
        else:
            st.error(f"Registration failed: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend server. Is it running?")

def logout():
    st.session_state.auth_token = None
    st.session_state.user_info = None
    st.rerun()

def get_user_info():
    if st.session_state.auth_token:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        try:
            response = requests.get(f"{API_URL}/users/me", headers=headers)
            if response.status_code == 200:
                st.session_state.user_info = response.json()
        except:
            pass

def save_scan(image_hash, disease_name, confidence, recommendation):
    if st.session_state.auth_token:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        payload = {
            "image_hash": image_hash,
            "disease_name": disease_name,
            "confidence": confidence,
            "recommendation": recommendation
        }
        try:
            requests.post(f"{API_URL}/scans", json=payload, headers=headers)
        except:
            pass

def get_scan_history():
    if st.session_state.auth_token:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        try:
            response = requests.get(f"{API_URL}/scans", headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            pass
    return []

# Auth Flow
if not st.session_state.auth_token:
    st.title("AgriGuard: Farmer Portal")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)
            
    with tab2:
        st.header("Register")
        new_email = st.text_input("Email")
        new_username = st.text_input("Username", key="reg_user")
        new_password = st.text_input("Password", type="password", key="reg_pass")
        new_fullname = st.text_input("Full Name")
        new_location = st.text_input("Farm Location")
        if st.button("Register"):
            register(new_email, new_username, new_password, new_fullname, new_location)

else:
    # Main App
    if not st.session_state.user_info:
        get_user_info()
    
    with st.sidebar:
        st.write(f"Welcome, **{st.session_state.user_info['full_name'] if st.session_state.user_info else 'Farmer'}**!")
        if st.button("Logout"):
            logout()
    
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

                    # Save Scan
                    if st.session_state.auth_token:
                        save_scan(file_hash, predicted_class_name, float(confidence_score), advice)
                        st.success("Scan saved to history!")

    # Dashboard / History
    st.markdown("---")
    st.header("Recent Scans")
    if st.session_state.auth_token:
        history = get_scan_history()
        if history:
            for scan in history:
                with st.expander(f"{scan['disease_name']} - {datetime.datetime.fromisoformat(scan['timestamp']).strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Confidence:** {scan['confidence']:.2%}")
                    st.write(f"**Recommendation:** {scan['recommendation']}")
                    st.caption(f"Image Hash: {scan['image_hash']}")
        else:
            st.info("No scan history found.")
    else:
        st.warning("Please login to view and save scan history.")