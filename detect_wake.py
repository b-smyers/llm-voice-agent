import pvporcupine
import pyaudio
import struct
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
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
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
        while self._running:
            pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            result = self.porcupine.process(pcm)
            if result >= 0:
                self.on_wake.emit()

    def stop(self):
        self._running = False
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        self.porcupine.delete()