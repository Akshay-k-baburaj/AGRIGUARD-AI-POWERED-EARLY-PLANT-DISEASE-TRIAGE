"""
Evaluation script for AgriGuard model.
Computes Accuracy, Precision, Recall, and F1-score on validation/test set.
"""

import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import numpy as np
from model import build_model

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
VAL_DIR = os.path.join(DATA_DIR, 'valid')
TEST_DIR = os.path.join(DATA_DIR, 'test')
MODEL_PATH = os.path.join(BASE_DIR, '../models/agriguard_model.pth')
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '../models/class_indices.json')
IMG_SIZE = 224
BATCH_SIZE = 32

def evaluate_model(data_dir, model_path, class_indices_path):
    """
    Evaluate the trained model on validation/test data.
    Returns metrics: Accuracy, Precision, Recall, F1-score
    """
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load class indices
    with open(class_indices_path, 'r') as f:
        class_to_idx = json.load(f)
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    num_classes = len(class_to_idx)
    
    # Data transforms
    val_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Load dataset
    print(f"Loading data from {data_dir}...")
    dataset = datasets.ImageFolder(data_dir, transform=val_transforms)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Build and load model
    print(f"Loading model from {model_path}...")
    model = build_model(num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    # Evaluation
    all_preds = []
    all_labels = []
    
    print("Evaluating model...")
    with torch.no_grad():
        for images, labels in data_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Convert to numpy arrays
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    # Calculate metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average='weighted', zero_division=0
    )
    
    # Per-class metrics
    precision_per_class, recall_per_class, f1_per_class, support = precision_recall_fscore_support(
        all_labels, all_preds, average=None, zero_division=0
    )
    
    # Print results
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(f"\nOverall Metrics:")
    print(f"  Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"  Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"  F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    print(f"\nPer-Class Metrics:")
    print(f"{'Class':<40} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 90)
    for i in range(num_classes):
        class_name = idx_to_class[i]
        print(f"{class_name:<40} {precision_per_class[i]:<12.4f} {recall_per_class[i]:<12.4f} {f1_per_class[i]:<12.4f} {support[i]:<10}")
    
    print("\n" + "="*60)
    print("Classification Report:")
    print("="*60)
    class_names = [idx_to_class[i] for i in range(num_classes)]
    print(classification_report(all_labels, all_preds, target_names=class_names, zero_division=0))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'per_class_metrics': {
            'precision': precision_per_class,
            'recall': recall_per_class,
            'f1': f1_per_class,
            'support': support
        },
        'class_names': class_names
    }

if __name__ == "__main__":
    # Evaluate on validation set
    print("Evaluating on Validation Set:")
    val_metrics = evaluate_model(VAL_DIR, MODEL_PATH, CLASS_INDICES_PATH)
    
    # Optionally evaluate on test set if it exists and has proper structure
    # Note: Test set might not have the same folder structure as train/valid
    # Uncomment below if test set is organized in ImageFolder format
    # if os.path.exists(TEST_DIR):
    #     print("\n\nEvaluating on Test Set:")
    #     test_metrics = evaluate_model(TEST_DIR, MODEL_PATH, CLASS_INDICES_PATH)

