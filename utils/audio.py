from scipy import signal
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile

SAMPLE_RATE = 16000

def play(sound_file=None, frequency=440, duration=0.2, sample_rate=44100):
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

def temp_wave_file(audio_np):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        sf.write(tmp_wav.name, audio_np, SAMPLE_RATE)
        tmp_filename = tmp_wav.name
    return tmp_filename

def resample(audio_np: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
    if original_rate == target_rate:
        return audio_np
    
    duration = len(audio_np) / original_rate
    target_length = int(duration * target_rate)
    
    resampled_data = signal.resample(audio_np, target_length)
    
    return resampled_data