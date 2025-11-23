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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'valid')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, '../models/agriguard_model.pth')
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '../models/class_indices.json')
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20  # Increased from 1 to allow proper training
LEARNING_RATE = 0.001
PATIENCE = 5  # Early stopping patience
MIN_DELTA = 0.001  # Minimum change to qualify as improvement

def train():
    # Device configuration
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data Transforms with more augmentation to reduce overfitting
    train_transforms = transforms.Compose([
        transforms.Resize((256, 256)),  # Slightly larger for random crop
        transforms.RandomCrop(IMG_SIZE),
        transforms.RandomRotation(30),  # Increased rotation
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),  # Added vertical flip
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),  # Color augmentation
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),  # Translation
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        transforms.RandomErasing(p=0.1)  # Random erasing for regularization
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
    # Use weight decay for regularization
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    # Learning rate scheduler to reduce LR when validation plateaus
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

    # Train with early stopping
    print("Starting training...")
    best_val_loss = float('inf')
    patience_counter = 0
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []
    
    for epoch in range(EPOCHS):
        # Training phase
        model.train()
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
            
            if (i + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}")

        train_accuracy = 100 * train_correct / train_total
        avg_train_loss = running_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        train_accs.append(train_accuracy)
        print(f"Epoch [{epoch+1}/{EPOCHS}] Training - Loss: {avg_train_loss:.4f}, Accuracy: {train_accuracy:.2f}%")
        
        # Validation phase
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_accuracy = 100 * val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        val_losses.append(avg_val_loss)
        val_accs.append(val_accuracy)
        print(f"Epoch [{epoch+1}/{EPOCHS}] Validation - Loss: {avg_val_loss:.4f}, Accuracy: {val_accuracy:.2f}%")
        
        # Learning rate scheduling
        old_lr = optimizer.param_groups[0]['lr']
        scheduler.step(avg_val_loss)
        current_lr = optimizer.param_groups[0]['lr']
        if current_lr < old_lr:
            print(f"✓ Learning rate reduced: {old_lr:.6f} → {current_lr:.6f}")
        else:
            print(f"Current Learning Rate: {current_lr:.6f}")
        
        # Early stopping
        if avg_val_loss < best_val_loss - MIN_DELTA:
            best_val_loss = avg_val_loss
            patience_counter = 0
            # Save best model
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"✓ Best model saved! (Validation Loss: {best_val_loss:.4f})")
        else:
            patience_counter += 1
            print(f"Early stopping patience: {patience_counter}/{PATIENCE}")
        
        if patience_counter >= PATIENCE:
            print(f"\nEarly stopping triggered after {epoch+1} epochs")
            print(f"Best validation loss: {best_val_loss:.4f}")
            break
        
        print("-" * 60)
    
    # Final summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    print(f"Total epochs trained: {epoch+1}")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Final training accuracy: {train_accs[-1]:.2f}%")
    print(f"Final validation accuracy: {val_accs[-1]:.2f}%")
    print(f"Model saved to: {MODEL_SAVE_PATH}")
    print("="*60)

if __name__ == "__main__":
    train()
