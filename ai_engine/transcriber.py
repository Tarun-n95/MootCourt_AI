import speech_recognition as sr
import os

def transcribe_audio(filepath):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_sphinx(audio_data)  # Offline recognition
            return text
    except Exception as e:
        print(f"Error transcribing: {e}")
        return ""

def grade_answer(transcribed_text, case_type):
    # Very basic grading: based on keyword matching
    keywords = {
        "Civil Law": ["contract", "tort", "damages", "negligence"],
        "Criminal Law": ["crime", "evidence", "intent", "conviction"],
        "Corporate Law": ["company", "shareholder", "compliance", "board"],
        "Family Law": ["custody", "divorce", "marriage", "maintenance"],
        "Constitutional Law": ["rights", "constitution", "review", "fundamental"],
        "Intellectual Property Law": ["copyright", "patent", "infringement", "trademark"]
    }

    keyword_list = keywords.get(case_type, [])
    found = sum(1 for word in keyword_list if word.lower() in transcribed_text.lower())

    # Scoring:
    if found == 0:
        return 2, "Try to use more legal terms related to your case."
    elif found <= 2:
        return 5, "Good attempt, but try including stronger legal terms."
    else:
        return 8, "Excellent! Your answer shows strong legal understanding."
