# Week 2 Day 2: Facial Recognition Model Training

Welcome to Week 2! Let's get our computer vision model running.

## Step 1: Point to Your Emotion Model
**File to edit:** `emotion_detector.py`
**Search for:** `@STUDENT-EDIT-Week2_Day2-1`

The game needs to know where to find the trained model weights.
**Hint:** If you captured your own face data and trained a new model in Google Colab, place the `.pth` file in the `ai_materials` folder, and change the file name in the `os.path.join()` call to match your model's name!

---

## Step 2: Adjust Confidence Thresholds
**File to edit:** `emotion_detector.py`
**Search for:** `@STUDENT-EDIT-Week2_Day2-2`

Sometimes the model is too confident about the wrong emotion.
**Hint:** Right below this comment, the model gets the maximum prediction. You can add an `if` statement to check if `torch.max(output)` is greater than a certain threshold (like 0.7 or 70%). If it's less, maybe set the emotion to "neutral" instead of guessing incorrectly!
