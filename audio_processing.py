import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine
r: sr.Recognizer = sr.Recognizer()
engine: pyttsx3.engine.Engine = pyttsx3.init()

# TODO: Add Documentation
def SpeakText(command: str):
    engine.say(command)
    engine.runAndWait()

# TODO: Add Documentation
def SpeechToText() -> str:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            # FIX: below line throws an error if only silence is detected for 3 seconds
            audio: sr.AudioData = r.listen(source, timeout=3, phrase_time_limit=5)
            text: str = r.recognize_google(audio).lower()
            return text
    except sr.UnknownValueError:        
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

if __name__ == "__main__":
    while True:
        result = SpeechToText()
        if(result != None):
            print(f"User said: {result}")