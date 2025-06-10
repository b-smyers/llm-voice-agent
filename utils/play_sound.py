import sounddevice as sd
import numpy as np
import soundfile as sf

def play_sound(sound_file=None, frequency=440, duration=0.2, sample_rate=44100):
    """
    Play a beep sound.
    If sound_file is provided, play the audio file.
    Otherwise, play a generated sine beep tone.
    """
    if sound_file:
        try:
            data, fs = sf.read(sound_file, dtype='float32')
            sd.play(data, samplerate=fs)
            sd.wait()
            return
        except Exception as e:
            print(f"Warning: Could not play beep file '{sound_file}': {e}")
            print("Falling back to generated beep tone.")

    # Generate and play sine wave beep
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    beep = 0.3 * np.sin(2 * np.pi * frequency * t)
    sd.play(beep, samplerate=sample_rate)
    sd.wait()