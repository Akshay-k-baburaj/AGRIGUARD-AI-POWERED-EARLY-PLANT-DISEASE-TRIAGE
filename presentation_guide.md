# AgriGuard Judge Presentation Guide

Since the code is already working, your goal is to demonstrate **ownership** and **understanding**. Here is a plan to impress the judges:

## 1. The "Live" Training Demo
Instead of just saying "we trained it," **show** them the training process starting.
*   **Action**: Open your terminal and run `python3 train.py`.
*   **What to say**: "Here is our training pipeline. We use a transfer learning approach with MobileNetV2. As you can see, it loads the data, applies augmentation, and begins optimizing the loss."
*   *Tip*: You can stop it after a few seconds (Ctrl+C) and say, "We've already trained the full model to save time, so let's jump to the results."

## 2. The "Live Coding" Feature (The "Magic" Trick)
Judges love seeing you modify code on the fly. It proves you didn't just copy it.
**Task**: Add a **Confidence Threshold Slider** to the sidebar.
*   **Scenario**: "Judges, sometimes the model isn't sure. I'll add a control right now to filter out low-confidence predictions."

### Step-by-Step Live Coding:
1.  Open `src/app.py`.
2.  Find the `st.sidebar.success(...)` line (around line 55).
3.  Add this code right after it:
    ```python
    confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    ```
4.  Scroll down to where you display the result (around line 85).
5.  Wrap the result display in an `if` statement:
    ```python
    if confidence_score < confidence_threshold:
        st.warning("⚠️ Confidence too low. Please upload a clearer image.")
    else:
        st.subheader("Result")
        # ... existing code ...
    ```
6.  Save the file. The app will update instantly (thanks to `watchdog`).
7.  **Show it off**: Slide the bar to 90% and show how a prediction might turn into a warning.

## 3. Explain the "Why" (Talking Points)
*   **Why MobileNet?**: "We chose it because it's lightweight. We want this to run on a farmer's cheap Android phone, not a $10,000 server."
*   **Why PyTorch?**: "It gives us dynamic computation graphs, making it easier to debug our model architecture during research."
*   **Why Hashing?**: "Data integrity is crucial. If a hacker corrupts the training images, our model fails. The SHA256 check ensures the input is valid."

## 4. Manual Verification
*   Open the `data/valid` folder.
*   Pick a tricky image (e.g., one with a busy background).
*   Run it through the app.
*   If it fails or succeeds, explain *why* (e.g., "The lighting here is poor, which affects the model's certainty").
