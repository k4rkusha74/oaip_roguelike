import winsound
import os

def get_sound(name_sound):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(current_dir, 'sounds', name_sound)

    # Воспроизводим звук
    winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)