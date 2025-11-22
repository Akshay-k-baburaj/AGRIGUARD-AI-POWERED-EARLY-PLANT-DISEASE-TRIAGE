# AgriGuard: AI-Powered Plant Disease Detection

AgriGuard is an AI-powered system for detecting plant diseases from leaf images. It uses a MobileNetV2 model trained on the PlantVillage dataset to classify images into 38 categories and provides agricultural recommendations.

## Features
- **Disease Detection**: Classifies 38 different plant/disease combinations.
- **Recommendations**: Provides actionable advice for each detected disease.
- **Dashboard**: User-friendly Streamlit interface.
- **Evaluation Metrics**: Comprehensive evaluation with Accuracy, Precision, Recall, and F1-score.
- **Security**: Verifies image integrity using SHA256 hashing.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Data**:
    Ensure your dataset is in `data/train` and `data/valid`.

## Usage

### Training
To train the model:
```bash
cd src
python3 train.py
```

### Dashboard
To run the web application:
```bash
cd src
streamlit run app.py
```

### Evaluation
To evaluate the model and get comprehensive metrics (Accuracy, Precision, Recall, F1-score):
```bash
cd src
python evaluate.py
```

### Jupyter Notebook Demo
To run the interactive demonstration notebook:
```bash
jupyter notebook demo.ipynb
```

## Model
The model is based on MobileNetV2 (pre-trained on ImageNet) and fine-tuned using PyTorch.

## Evaluation Metrics
The evaluation script provides:
- Overall Accuracy, Precision, Recall, and F1-Score
- Per-class metrics for all 38 disease categories
- Detailed classification report
