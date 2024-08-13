from subprocess import Popen
import speech_recognition as sr

# Initialize the recognizer and text-to-speech engine
speech_recognizer: sr.Recognizer = None

# TODO: Add Documentation
def SpeakText(command: str):
    Popen(["python", "text_to_speech.py", command])

def load_speech_capture():
    global speech_recognizer
    speech_recognizer = sr.Recognizer()

# TODO: Add Documentation
def capture_speech() -> str:
    if(speech_recognizer == None):
        raise Exception("Recognizer not loaded, call audio_load() first.")
    try:
        with sr.Microphone() as source:
            print("Listening...")
            speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
           
            audio: sr.AudioData = speech_recognizer.listen(source, timeout=3, phrase_time_limit=5)
            text: str = speech_recognizer.recognize_google(audio).lower()
            return text
    except sr.UnknownValueError:        
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")
        return None

def list_microphones():
  """Lists all available microphones on the system"""
  for i, name in enumerate(sr.Microphone.list_microphone_names()):
      print(f"{i}: {name}")

if __name__ == "__main__":
  list_microphones()
