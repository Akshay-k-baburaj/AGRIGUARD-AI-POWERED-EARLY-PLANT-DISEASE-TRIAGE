import torch
import torch.nn.functional as F
import cv2
import numpy as np

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        
        # Hook for gradients
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)

    def save_activation(self, module, input, output):
        self.activation = output

    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def __call__(self, x, class_idx=None):
        # Forward pass
        self.model.eval()
        output = self.model(x)
        
        if class_idx is None:
            class_idx = torch.argmax(output, dim=1)

        # Backward pass
        self.model.zero_grad()
        class_loss = output[0, class_idx]
        class_loss.backward()

        # Generate CAM
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activation = self.activation[0]
        
        for i in range(activation.shape[0]):
            activation[i, :, :] *= pooled_gradients[i]
            
        heatmap = torch.mean(activation, dim=0).cpu().detach().numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap /= torch.max(torch.tensor(heatmap)) if torch.max(torch.tensor(heatmap)) != 0 else 1
        
        return heatmap

def get_gradcam_heatmap(model, input_tensor, original_image):
    """
    Generates Grad-CAM heatmap and overlays it on the original image.
    """
    # Target the last convolutional layer of features
    # MobileNetV2 features end with a Conv2dBNActivation block
    target_layer = model.features[-1]
    
    grad_cam = GradCAM(model, target_layer)
    
    # Enable grad for CAM generation even in eval mode
    with torch.enable_grad():
        heatmap = grad_cam(input_tensor)
        
    # Resize heatmap to image size
    heatmap = cv2.resize(heatmap, (original_image.width, original_image.height))
    
    # Colorize
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Overlay
    original_np = np.array(original_image)
    superimposed_img = heatmap * 0.4 + original_np * 0.6
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    
    return superimposed_img
