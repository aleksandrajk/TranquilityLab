import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from utils import compute_fft

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

plt.ion()
fig, ax = plt.subplots()
bars = ax.bar(np.arange(50), np.zeros(50))
ax.set_ylim(0, 50)

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    mono = np.mean(indata, axis=1)
    freqs, magnitudes = compute_fft(mono, SAMPLE_RATE)
    bins = np.array_split(magnitudes, 50)
    avg_bins = [np.mean(b) for b in bins]

    for bar, h in zip(bars, avg_bins):
        bar.set_height(h)

    plt.pause(0.001)

def start_visualizer():
    with sd.InputStream(channels=2,
                        callback=audio_callback,
                        blocksize=BLOCK_SIZE,
                        samplerate=SAMPLE_RATE):
        print("🎶 Visualizing... press Ctrl+C to stop.")
        while True:
            sd.sleep(1000)

if __name__ == "__main__":
    start_visualizer()
