import pyttsx3
import random
import json
import os

# Load narrations (text prompts for motivational speeches)
def load_narrations():
    with open("narrations.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Pick one narration at random
def pick_narration():
    narrations = load_narrations()
    return random.choice(narrations)

# Generate speech audio
def generate_voice(text, out_path="narration.mp3"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)  # speed of speech
    engine.setProperty("volume", 1.0)  # max volume
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)  # pick a voice
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    return out_path

if __name__ == "__main__":
    narration = pick_narration()
    print("🎙 Narrating:", narration)
    path = generate_voice(narration)
    print("✅ Audio saved at:", path)
