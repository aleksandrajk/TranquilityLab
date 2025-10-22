import argparse
import sys
import signal
from audio_analyzer import AudioAnalyzer
from osc_manager import OSCManager

def signal_handler(sig, frame):
    print("\nShutting down TranquilityLab...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='TranquilityLab Audio Visualizer')
    parser.add_argument('--osc-ip', default='127.0.0.1', help='OSC target IP')
    parser.add_argument('--osc-port', type=int, default=8000, help='OSC target port')
    parser.add_argument('--receive-port', type=int, default=8001, help='OSC receive port')
    parser.add_argument('--sample-rate', type=int, default=44100, help='Audio sample rate')
    parser.add_argument('--block-size', type=int, default=1024, help='Audio block size')
    
    args = parser.parse_args()
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🌌🎶 Starting TranquilityLab...")
    print(f"OSC Target: {args.osc_ip}:{args.osc_port}")
    print(f"OSC Receive: {args.osc_ip}:{args.receive_port}")
    
    try:
        # Initialize OSC manager
        osc_mgr = OSCManager(
            send_ip=args.osc_ip,
            send_port=args.osc_port,
            receive_port=args.receive_port
        )
        osc_mgr.start_receiver()
        
        # Initialize audio analyzer with OSC client
        analyzer = AudioAnalyzer(
            osc_client=osc_mgr.client,
            sample_rate=args.sample_rate,
            block_size=args.block_size
        )
        
        print("\nAudio-reactive visuals system ready!")
        print("Press Ctrl+C to stop\n")
        
        # Start audio stream (this will block until interrupted)
        analyzer.start_stream()
        
    except Exception as e:
        print(f"Failed to start TranquilityLab: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
