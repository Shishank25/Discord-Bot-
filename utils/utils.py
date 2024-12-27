import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking speed (default: 200)
engine.setProperty('volume', 0.50)  # Adjust volume (0.0 to 1.0)

def text_to_speech(text, filename="speech.mp3"):
    engine.save_to_file(text, filename)
    engine.runAndWait()

def parse_time(time_str: str) -> int:
    unit = time_str[-1]
    value = int(time_str[:-1])

    if unit == 's':
        return value

    elif unit == 'm':
        return value * 60
        
    elif unit == 'h':
        return value * 60 * 60

    else:
        return None