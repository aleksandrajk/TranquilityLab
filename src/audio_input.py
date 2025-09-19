import numpy as np
import sounddevice as sd
from utils import compute_fft, send_via_osc

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    mono = np.mean(indata, axis=1)  # convert to mono
    freqs, magnitudes = compute_fft(mono, SAMPLE_RATE)
    send_via_osc(magnitudes.tolist())  # send to TD or visualizer

def start_audio_stream():
    with sd.InputStream(channels=2,
                        callback=audio_callback,
                        blocksize=BLOCK_SIZE,
                        samplerate=SAMPLE_RATE):
        print("🎵 Listening... press Ctrl+C to stop.")
        while True:
            sd.sleep(1000)

if __name__ == "__main__":
    start_audio_stream()
