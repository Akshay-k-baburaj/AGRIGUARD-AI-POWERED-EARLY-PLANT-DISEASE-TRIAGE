import torch
import torch.nn as nn
from torchvision import models

def build_model(num_classes):
    """
    Builds a MobileNetV2 based model for transfer learning using PyTorch.
    """
    # Load pre-trained MobileNetV2
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    # Freeze parameters
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace the classifier head with dropout for regularization
    # MobileNetV2 classifier is a Sequential block with Dropout and Linear
    # Keep dropout at 0.2 for regularization
    model.classifier = nn.Sequential(
        nn.Dropout(0.2),  # Dropout for regularization
        nn.Linear(model.last_channel, num_classes)
    )
    
    return model

if __name__ == "__main__":
    model = build_model(num_classes=38)
    print(model)
