import numpy as np
import sounddevice as sd
from scipy.fft import fft
from pythonosc import udp_client
import time
import sys

class AudioAnalyzer:
    def __init__(self, osc_client=None, sample_rate=44100, block_size=1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.osc_client = osc_client
        self.audio_data = np.zeros(block_size)
        self.volume_history = []
        
        # Frequency bands (Hz)
        self.bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'brilliance': (6000, 20000)
        }
        
    def audio_callback(self, indata, frames, time, status):
        """Main audio processing callback"""
        if status:
            print(f"Audio callback status: {status}")
            
        # Get mono audio data
        if indata.ndim > 1:
            self.audio_data = indata[:, 0]
        else:
            self.audio_data = indata.flatten()
            
        # Analyze audio
        analysis = self.analyze_audio(self.audio_data)
        
        # Send OSC data if client exists
        if self.osc_client:
            self.send_osc_data(analysis)
            
    def analyze_audio(self, audio_data):
        """Perform FFT analysis and extract features"""
        analysis = {}
        
        # Calculate RMS volume
        analysis['volume'] = np.sqrt(np.mean(audio_data**2))
        
        # Apply Hanning window to reduce spectral leakage
        window = np.hanning(len(audio_data))
        windowed_data = audio_data * window
        
        # Perform FFT
        fft_data = fft(windowed_data)
        freqs = np.fft.fftfreq(len(fft_data), 1.0/self.sample_rate)
        
        # Get magnitude spectrum (only positive frequencies)
        magnitude = np.abs(fft_data[:len(fft_data)//2])
        freqs = freqs[:len(freqs)//2]
        
        # Analyze frequency bands
        for band_name, (low_freq, high_freq) in self.bands.items():
            band_mask = (freqs >= low_freq) & (freqs <= high_freq)
            if np.any(band_mask):
                band_energy = np.mean(magnitude[band_mask])
                analysis[band_name] = float(band_energy)
            else:
                analysis[band_name] = 0.0
                
        # Beat detection (simple onset detection)
        analysis['onset'] = self.detect_onset(analysis['volume'])
        
        return analysis
    
    def detect_onset(self, current_volume):
        """Simple beat/onset detection"""
        self.volume_history.append(current_volume)
        if len(self.volume_history) > 10:  # Keep last 10 frames
            self.volume_history.pop(0)
            
        if len(self.volume_history) >= 5:
            avg_volume = np.mean(self.volume_history[:-3])  # Average of older volumes
            if current_volume > avg_volume * 2.0:  # Sudden increase
                return 1.0
        return 0.0
    
    def send_osc_data(self, analysis):
        """Send analysis data via OSC"""
        try:
            # Send volume and beat data
            self.osc_client.send_message("/audio/volume", analysis['volume'])
            self.osc_client.send_message("/audio/onset", analysis['onset'])
            
            # Send frequency bands
            for band_name, value in analysis.items():
                if band_name not in ['volume', 'onset']:
                    self.osc_client.send_message(f"/audio/bands/{band_name}", value)
                    
            # Send raw FFT data for visualization (downsampled)
            if 'fft_magnitude' in analysis:
                fft_downsampled = analysis['fft_magnitude'][::8]  # Downsample by 8
                for i, value in enumerate(fft_downsampled[:64]):  # Send first 64 points
                    self.osc_client.send_message(f"/audio/fft/{i}", float(value))
                    
        except Exception as e:
            print(f"OSC send error: {e}")
    
    def start_stream(self):
        """Start the audio stream"""
        try:
            print("Starting audio stream...")
            print("Available audio devices:")
            print(sd.query_devices())
            
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                latency='low'
            ):
                print("Audio stream started! Press Ctrl+C to stop.")
                while True:
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            print("\nTroubleshooting tips:")
            print("1. Check your audio device ID")
            print("2. Make sure no other app is using the microphone")
            print("3. Try different sample rate or block size")

if __name__ == "__main__":
    # Test the analyzer
    analyzer = AudioAnalyzer()
    test_data = np.random.random(1024) * 0.1
    result = analyzer.analyze_audio(test_data)
    print("Test analysis:", {k: f"{v:.4f}" for k, v in result.items()})
