import numpy as np
from pythonosc import udp_client

# OSC client for TouchDesigner (default localhost:5005)
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

def compute_fft(signal, sample_rate):
    spectrum = np.fft.rfft(signal)
    magnitude = np.abs(spectrum)
    freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
    return freqs, magnitude

def send_via_osc(data, address="/audio"):
    try:
        osc_client.send_message(address, data)
    except Exception as e:
        print(f"OSC send failed: {e}")
