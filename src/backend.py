import torch
from torchvision import transforms
from PIL import Image
import json
import os
from model import build_model

class AgriGuardModel:
    """Handles model loading and predictions"""
    
    def __init__(self, model_path, class_indices_path):
        self.model_path = model_path
        self.class_indices_path = class_indices_path
        self.model = None
        self.device = None
        self.class_indices = None
        
    def load_class_indices(self):
        """Load class indices from JSON file"""
        if not os.path.exists(self.class_indices_path):
            return None
        with open(self.class_indices_path, 'r') as f:
            class_indices = json.load(f)
        # Invert: Name -> Index to Index -> Name
        return {v: k for k, v in class_indices.items()}
    
    def load_model(self):
        """Load the trained model"""
        self.class_indices = self.load_class_indices()
        
        if self.class_indices is None:
            return False
            
        num_classes = len(self.class_indices)
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.model = build_model(num_classes)
        
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            return True
        return False
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        return transform(image).unsqueeze(0).to(self.device)
    
    def predict(self, image):
        """Make prediction on image"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        input_tensor = self.preprocess_image(image)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        predicted_class_index = predicted.item()
        predicted_class_name = self.class_indices[predicted_class_index]
        confidence_score = confidence.item()
        
        return predicted_class_name, confidence_score