import pyaudio
  
    
class FromMicrophone:
    def __init__(self, chunk_seconds, channels: int = 1, sr: int = 16000) -> None:
        self.chunk_size = int(chunk_seconds * sr)
        self.channels = channels
        self.sr = sr
        self.format_audio = pyaudio.paInt16
        self.p = pyaudio.PyAudio()

    def __enter__(self):
        self.stream = self.p.open(
            format=self.format_audio,
            channels=self.channels,
            rate=self.sr,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        print('Stream has been started')
        return self.stream

    def __exit__(self, type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        print('Stream has been finished')
