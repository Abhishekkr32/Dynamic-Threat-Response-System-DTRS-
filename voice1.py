import pyttsx3

def voice_alert(process_name):
    engine = pyttsx3.init()
    engine.say(f"Warning! {process_name} detected and terminated.")
    engine.runAndWait()
