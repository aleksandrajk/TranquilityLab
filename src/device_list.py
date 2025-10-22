import sounddevice as sd

def list_audio_devices():
    """List all available audio devices"""
    devices = sd.query_devices()
    print("\nAvailable Audio Devices:")
    print("-" * 50)
    
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")
        print(f"   Input Channels: {device['max_input_channels']}")
        print(f"   Output Channels: {device['max_output_channels']}")
        print(f"   Default Sample Rate: {device['default_samplerate']}")
        print()

if __name__ == "__main__":
    list_audio_devices()
