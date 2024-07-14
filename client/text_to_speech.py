import sys
import pyttsx3

# TODO: Add Documentation
def init_engine():
    engine = pyttsx3.init()
    return engine

# TODO: Add Documentation
def say(s):
    engine.say(s)
    engine.runAndWait() 

# TODO: Add Documentation
if __name__ == "__main__":
    engine = init_engine()
    say(str(sys.argv[1]))
