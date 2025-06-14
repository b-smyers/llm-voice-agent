import tempfile
import wave
import os

import pyaudio
import numpy as np
import soundfile as sf
from scipy import signal

SAMPLE_RATE = 16000

def play(sound_file=None, frequency=440, duration=0.2, sample_rate=44100):
    p = pyaudio.PyAudio()

    if sound_file and os.path.exists(sound_file):
        try:
            wf = wave.open(sound_file, 'rb')
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)

            stream.stop_stream()
            stream.close()
            wf.close()
            p.terminate()
            return
        except Exception as e:
            print(f"Warning: Could not play beep file '{sound_file}': {e}")
            print("Falling back to generated beep tone.")

    # Generate and play sine wave beep
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    beep = 0.3 * np.sin(2 * np.pi * frequency * t)  # amplitude 0.3 to prevent clipping

    # Convert to 16-bit PCM
    beep_pcm = (beep * 32767).astype(np.int16).tobytes()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True
    )

    stream.write(beep_pcm)
    stream.stop_stream()
    stream.close()
    p.terminate()

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