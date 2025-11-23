# How to Run and Use the Jupyter Notebook

## Prerequisites

1. **Install Jupyter Notebook** (if not already installed):
   ```bash
   pip install jupyter notebook
   ```
   Or if you prefer JupyterLab:
   ```bash
   pip install jupyterlab
   ```

2. **Ensure all dependencies are installed**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure you have a trained model**:
   - The model should be at: `models/agriguard_model.pth`
   - If not, train it first: `cd src && python train.py`

## Running the Notebook

### Method 1: Using Jupyter Notebook (Classic)

1. **Navigate to the project directory**:
   ```bash
   cd /Users/samarthyajambavalikar/Desktop/AgriGuard/AGRIGUARD-AI-POWERED-EARLY-PLANT-DISEASE-TRIAGE
   ```

2. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```
   This will open Jupyter in your web browser.

3. **Open the notebook**:
   - Click on `demo.ipynb` in the file browser

### Method 2: Using JupyterLab

1. **Navigate to the project directory**:
   ```bash
   cd /Users/samarthyajambavalikar/Desktop/AgriGuard/AGRIGUARD-AI-POWERED-EARLY-PLANT-DISEASE-TRIAGE
   ```

2. **Start JupyterLab**:
   ```bash
   jupyter lab
   ```

3. **Open the notebook**:
   - Double-click `demo.ipynb` in the file browser

### Method 3: Using VS Code / Cursor

1. **Open the notebook file**:
   - The notebook should open directly in VS Code/Cursor
   - You'll see cells that can be run individually

2. **Run cells**:
   - Click the "Run" button above each cell
   - Or use `Shift + Enter` to run a cell and move to the next

## How to Use the Notebook

### Step-by-Step Execution

1. **Run Cell 1** (Imports and Setup):
   - This loads all necessary libraries
   - Sets up paths to model and class indices
   - **Expected output**: "AgriGuard Demo - Plant Disease Detection"

2. **Run Cell 3** (Load Class Indices):
   - Loads the class mapping file
   - **Expected output**: Number of classes and sample class names

3. **Run Cell 4** (Load Model):
   - Loads the trained model into memory
   - **Expected output**: Device being used and "Model loaded successfully!"

4. **Run Cell 6** (Define Functions):
   - Defines helper functions for image processing and classification
   - No output expected

5. **Run Cell 8** (Classify an Image):
   - This is the main classification cell
   - **You can modify the image path** to test different images
   - **Expected output**: 
     - Image visualization
     - Classification results with confidence scores
     - Top 3 predictions

6. **Run Cell 10** (Get Recommendations):
   - Shows agricultural recommendations for the predicted disease
   - **Expected output**: Recommendation text

7. **Run Cell 12** (Batch Processing):
   - Processes multiple images at once
   - Creates a results table
   - **Expected output**: Pandas DataFrame with results

## Customizing the Notebook

### Testing Your Own Images

**Option 1: Use images from the test folder**
```python
# In Cell 8, change the path:
test_image_path = "data/test/YourImageName.JPG"
```

**Option 2: Use your own images**
```python
# Place your image in the project root or a folder, then:
test_image_path = "path/to/your/image.jpg"
```

**Option 3: Upload images interactively**
Add this cell before Cell 8:
```python
from IPython.display import display, FileLink
import ipywidgets as widgets

upload = widgets.FileUpload(accept='.jpg,.jpeg,.png', multiple=False)
display(upload)

# After uploading, save and use:
if upload.value:
    filename = list(upload.value.keys())[0]
    with open(f"temp_{filename}", "wb") as f:
        f.write(upload.value[filename]['content'])
    test_image_path = f"temp_{filename}"
```

### Processing Multiple Custom Images

In Cell 12, modify the path:
```python
# Process images from a custom folder
test_dir = Path("path/to/your/images")
test_images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.JPG"))
```

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure you're running from the project root directory and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Model not found"
**Solution**: Train the model first:
```bash
cd src
python train.py
```

### Issue: "Image not found"
**Solution**: Check that the image path is correct. Use absolute paths if needed:
```python
import os
test_image_path = os.path.abspath("data/test/TomatoHealthy1.JPG")
```

### Issue: Kernel keeps restarting
**Solution**: The model might be too large for your system. Try:
- Restart the kernel
- Run cells one at a time
- Close other applications to free up memory

### Issue: Matplotlib plots not showing
**Solution**: Add this at the beginning (Cell 1):
```python
%matplotlib inline
```

## Tips

1. **Run cells in order**: The notebook is designed to run sequentially
2. **Check outputs**: Each cell should produce expected output before moving to the next
3. **Save frequently**: Use `Ctrl+S` (or `Cmd+S` on Mac) to save the notebook
4. **Restart kernel if needed**: If something goes wrong, use "Kernel > Restart & Clear Output"

## Quick Start (Copy-Paste)

If you want to quickly test a single image, you can run this in a new cell:

```python
# Quick test cell
image_path = "data/test/TomatoHealthy1.JPG"  # Change this

# Verify integrity
file_hash = calculate_sha256(image_path)
print(f"Hash: {file_hash[:16]}...")

# Classify
input_tensor, img = preprocess_image(image_path)
predicted, conf, top3 = classify_image(model, input_tensor)
rec = get_recommendation(predicted)

# Display
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title(f"{predicted}\nConfidence: {conf:.2%}")
plt.axis('off')
plt.subplot(1, 2, 2)
plt.text(0.1, 0.9, f"Prediction: {predicted}", fontsize=12, transform=plt.gca().transAxes)
plt.text(0.1, 0.8, f"Confidence: {conf:.2%}", fontsize=12, transform=plt.gca().transAxes)
plt.text(0.1, 0.6, "Recommendation:", fontsize=11, weight='bold', transform=plt.gca().transAxes)
plt.text(0.1, 0.5, rec, fontsize=10, transform=plt.gca().transAxes, wrap=True)
plt.axis('off')
plt.tight_layout()
plt.show()
```

## Next Steps

- Try different images from the test folder
- Experiment with batch processing
- Modify the visualization style
- Add your own analysis cells

