from playsound import playsound
import time
from config import SHORT_SOUND, LONG_SOUND

def play_sound(codes):
    for code in codes:
        if code == '•':
            playsound(SHORT_SOUND)
        elif code == '−':
            playsound(LONG_SOUND)
        elif code == ' ':
            time.sleep(1)
        time.sleep(0.1)