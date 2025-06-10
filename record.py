from utils.play_sound import play_sound
import sounddevice as sd
import numpy as np
import queue

beep_start_path = "sounds/record_start.wav"
beep_end_path = "sounds/record_end.wav"

SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30
FRAMES_PER_SAMPLE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
SILENCE_THRESHOLD_SEC = 1.5

q = queue.Queue()

def record():
    buffer = []
    silence_start = None

    def callback(indata, frames, time, status):
        audio = indata[:, 0]
        q.put(audio.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=FRAMES_PER_SAMPLE) as stream:
        play_sound(sound_file=beep_start_path)
        while True:
            audio = q.get()
            buffer.append(audio)
            energy = np.abs(audio).mean()
            if energy < 0.01:
                if silence_start is None:
                    silence_start = stream.time
                elif stream.time - silence_start > SILENCE_THRESHOLD_SEC:
                    break
            else:
                silence_start = None
        play_sound(sound_file=beep_end_path)

    audio_np = np.concatenate(buffer)
    return audio_np