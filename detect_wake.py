import pvporcupine
import sounddevice as sd
import numpy as np
import os
from threading import Thread

# Simple Event class
class Event:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def emit(self, *args, **kwargs):
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)

class WakeListener:
    def __init__(self, keyword_path):
        self.keyword_path = keyword_path
        self.porcupine = pvporcupine.create(
            access_key=os.getenv('PICOVOICE_API_KEY'),
            keyword_paths=[self.keyword_path]
        )

        # Events
        self.on_ready = Event()
        self.on_wake = Event()
        self._running = False

    def start(self):
        self._running = True
        Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        self.on_ready.emit()
        def audio_callback(indata, frames, time, status):
            if not self._running:
                return
            pcm = np.int16(indata[:, 0] * 32768)  # Convert float32 [-1,1] to int16
            pcm = pcm[:self.porcupine.frame_length]  # Match Porcupine's expected frame size
            result = self.porcupine.process(pcm)
            if result >= 0:
                self.on_wake.emit()

        with sd.InputStream(
            samplerate=self.porcupine.sample_rate,
            blocksize=self.porcupine.frame_length,
            dtype='float32',
            channels=1,
            callback=audio_callback
        ):
            while self._running:
                sd.sleep(100)  # keep thread alive

    def stop(self):
        self._running = False
        self.porcupine.delete()