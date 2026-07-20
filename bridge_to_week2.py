"""
bridge_to_week2.py - From Your Python to Real AI
================================================
This little script is the "capstone" that connects everything you learned in Week 1 to
the AI you will build in Week 2.

In Week 2, the game will:
  1. Watch you through the webcam,
  2. Use a trained AI MODEL to guess your EMOTION (happy, sad, angry, ...),
  3. Send that emotion to a Large Language Model to generate an NPC's reply.

That whole pipeline is just:   INPUT  ->  MODEL  ->  PREDICTION  ->  ACTION

The tiny function below has the SAME shape, but uses only Week-1 Python (variables, a
list, a dictionary, a function, .get(), and f-strings). It takes an emotion and returns
a line the shopkeeper might say. In Week 2, you'll replace the hand-written dictionary
with a REAL AI model!

Run it with:   python bridge_to_week2.py
"""

# @STUDENT-EDIT-Day5-4: This dictionary maps an emotion (the INPUT) to a reply (the
# OUTPUT). In Week 2, a real AI model + Large Language Model replaces this simple lookup.
# Try adding your own emotions and lines, or change what the shopkeeper says!
EMOTION_REPLIES = {
    "happy": "You're glowing today! Your crops must be thriving. What can I get you?",
    "sad": "Chin up, friend. Every capitalist has hard days - let me help brighten yours.",
    "angry": "Take a breath. Farming tests our patience, but you're doing great.",
    "surprised": "Ha! Something catch you off guard? The farm is full of surprises.",
    "fearful": "You're safe here with me. No need to worry - let's get you sorted.",
    "neutral": "Good day! Let me know if you need seeds or tools.",
}


def respond_to_emotion(emotion):
    """Take a detected emotion label and return an NPC reply that matches it."""
    # .get() returns the matching reply, or a safe default if the emotion is unknown.
    return EMOTION_REPLIES.get(emotion, "Hello there! Nice day for farming.")


# Try the function on a list of emotions (like the ones the Week-2 model will detect).
# "confused" is not in our dictionary on purpose - watch the default reply kick in!
if __name__ == "__main__":
    detected_emotions = ["happy", "sad", "angry", "neutral", "confused"]
    for emotion in detected_emotions:
        reply = respond_to_emotion(emotion)
        print(f"[{emotion}] -> {reply}")
