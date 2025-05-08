import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    
    # You can customize voice properties
    engine.setProperty('rate', 150)     # Speed (lower is slower)
    engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female voice usually

    engine.say(text)
    engine.runAndWait()