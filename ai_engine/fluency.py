# ai_engine/fluency.py

def analyze_fluency(transcribed_text):
    if not transcribed_text:
        return 0, "No speech detected."

    words = transcribed_text.split()
    word_count = len(words)

    # --- Basic Pause Detection ---
    pause_words = ['uh', 'um', 'er', 'ah', 'hmm']
    pause_count = sum(1 for word in words if word.lower() in pause_words)

    # --- Sentence Length ---
    sentences = transcribed_text.split('.')
    avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / max(len(sentences), 1)

    # --- Words Per Minute (WPM) Estimate ---
    # Assuming each oral answer is about 1 minute for simplicity
    wpm = word_count  

    # --- Fluency Scoring Logic ---
    fluency_score = 10  # Start with perfect

    if wpm < 80:
        fluency_score -= 2  # Penalize slow speaking
    if pause_count > 5:
        fluency_score -= 2  # Too many pauses
    if avg_sentence_length < 6:
        fluency_score -= 2  # Very short, broken sentences

    fluency_score = max(0, min(10, fluency_score))  # Clamp between 0 and 10

    # --- Feedback ---
    feedback = []
    if wpm < 80:
        feedback.append("Try speaking a little faster.")
    if pause_count > 5:
        feedback.append("Reduce the number of filler words like 'uh', 'um'.")
    if avg_sentence_length < 6:
        feedback.append("Form longer, more complete sentences.")
    if fluency_score >= 8:
        feedback.append("Excellent fluency!")

    return fluency_score, " ".join(feedback)