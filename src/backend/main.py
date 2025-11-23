from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from . import models, schemas, auth, database
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AgriGuard Backend")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
    "http://10.10.43.61:8080",
    "http://10.10.43.61:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        farm_location=user.farm_location,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/scans", response_model=schemas.ScanOut)
def create_scan(scan: schemas.ScanCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_scan = models.Scan(**scan.dict(), user_id=current_user.id)
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return new_scan

@app.get("/scans", response_model=list[schemas.ScanOut])
def read_scans(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    scans = db.query(models.Scan).filter(models.Scan.user_id == current_user.id).order_by(models.Scan.timestamp.desc()).offset(skip).limit(limit).all()
    return scans

# Inference Setup
import torch
from torchvision import transforms
from PIL import Image
import io
import os
import json
from fastapi import UploadFile, File
from .model import build_model
from .recommend import get_recommendation
from .utils import calculate_sha256_bytes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Assuming src/backend/main.py, so ../../models is correct relative to this file
MODEL_PATH = os.path.join(BASE_DIR, "../../models/agriguard_model.pth")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "../../models/class_indices.json")

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
class_indices = {}
model = None

def load_resources():
    global model, class_indices
    if os.path.exists(CLASS_INDICES_PATH):
        with open(CLASS_INDICES_PATH, 'r') as f:
            indices = json.load(f)
            class_indices = {v: k for k, v in indices.items()}
    
    if class_indices:
        model = build_model(len(class_indices))
        if os.path.exists(MODEL_PATH):
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
            model.to(device)
            model.eval()
            print("Model loaded successfully.")
        else:
            print("Model file not found.")
    else:
        print("Class indices not found.")

# Load resources on startup
load_resources()

@app.post("/analyze")
async def analyze_plant(
    file: UploadFile = File(...), 
    x_file_hash: str | None = Header(default=None),
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Read image
    contents = await file.read()
    # Calculate hash
    file_hash = calculate_sha256_bytes(contents)
    
    # Integrity Check: If client provided a hash, verify it matches
    # This ensures the file wasn't corrupted in transit
    if x_file_hash and x_file_hash.lower() != file_hash.lower():
        raise HTTPException(
            status_code=400, 
            detail="Data Integrity Error: File hash mismatch. The file may have been corrupted during transfer."
        )

    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Data Integrity Error: Invalid image file. {str(e)}"
        )
    
    # Preprocess
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    # Predict
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
    predicted_class_index = predicted.item()
    predicted_class_name = class_indices.get(predicted_class_index, "Unknown")
    confidence_score = confidence.item()
    
    print(f"DEBUG: Predicted Class: {predicted_class_name}, Confidence: {confidence_score}")
    
    recommendation = get_recommendation(predicted_class_name)
    
    # Save scan
    new_scan = models.Scan(
        image_hash=file_hash,
        disease_name=predicted_class_name,
        confidence=confidence_score,
        recommendation=recommendation,
        user_id=current_user.id
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    
    return {
        "id": new_scan.id,
        "disease_name": predicted_class_name,
        "confidence": confidence_score,
        "recommendation": recommendation,
        "timestamp": new_scan.timestamp,
        "image_hash": file_hash
    }

