import os
from pydub import AudioSegment
from config import SHORT_SOUND, LONG_SOUND, EXPORT_FOLDER
import pygame

pygame.mixer.init()
def create_sound(input):
    if not input:
        return None

    audio = AudioSegment.silent(duration=0)
    for i in input:
        if i == '•' or i == '.':
            short_sound = AudioSegment.from_wav(SHORT_SOUND)
            audio += short_sound
        elif i == '−' or i == '-':
            long_sound = AudioSegment.from_wav(LONG_SOUND)
            audio += long_sound
        elif i == ' ':
            audio += AudioSegment.silent(duration=1000)  
        audio += AudioSegment.silent(duration=200)     
    return audio

def play_sound(input):
    if not input:
        return
    
    temp_path = os.path.join(os.path.dirname(__file__), "temp.wav")
    audio = create_sound(input)
    
    if audio:
        audio.export(temp_path, format="wav")
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)

        pygame.mixer.music.unload()
        os.remove(temp_path)

def download_sound(input,file_name):
    if not input:
        return
    
    file_name = clear_filename(file_name[:20])
    file_path = os.path.join(EXPORT_FOLDER, f'{file_name}.wav')

    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    audio = create_sound(input)
    if audio:
        audio.export(file_path, format="wav")
        print(f"File saved: {file_path}")

def clear_filename(text):
    invalid_chars = '/:*?"\<>|'

    for char in invalid_chars:
        text = text.replace(char, '_')
    return text