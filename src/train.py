import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from model import build_model
import ssl

# Disable SSL verification for model download
ssl._create_default_https_context = ssl._create_unverified_context

# Configuration
DATA_DIR = '../data'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'valid')
MODEL_SAVE_PATH = '../models/agriguard_model.pth'
CLASS_INDICES_PATH = '../models/class_indices.json'
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 1
LEARNING_RATE = 0.001

def train():
    # Device configuration
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data Transforms
    train_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomRotation(20),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Datasets
    print(f"Loading training data from {TRAIN_DIR}...")
    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transforms)
    
    print(f"Loading validation data from {VAL_DIR}...")
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transforms)

    # Data Loaders
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    num_classes = len(train_dataset.classes)
    print(f"Detected {num_classes} classes.")

    # Save class indices
    class_indices = {v: k for k, v in train_dataset.class_to_idx.items()} # Index to Name? No, usually Name to Index.
    # ImageFolder class_to_idx is Name -> Index.
    # We want to save Name -> Index so we can reverse it later.
    with open(CLASS_INDICES_PATH, 'w') as f:
        json.dump(train_dataset.class_to_idx, f)
    print(f"Saved class indices to {CLASS_INDICES_PATH}")

    # Build Model
    model = build_model(num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=LEARNING_RATE)

    # Train
    print("Starting training...")
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        # Limit steps for demo
        steps = 0
        max_steps = 10 

        for images, labels in train_loader:
            if steps >= max_steps:
                break
            steps += 1

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            if steps % 5 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}], Step [{steps}/{max_steps}], Loss: {loss.item():.4f}")

        print(f"Epoch [{epoch+1}/{EPOCHS}] Training Accuracy: {100 * correct / total:.2f}%")

    # Save Model
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()
