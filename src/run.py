#!/usr/bin/env python3
"""
TranquilityLab Quick Start
Run this script to start the audio visualization system
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting TranquilityLab...")
    
    # Check if requirements are installed
    try:
        import pythonosc, sounddevice, numpy, scipy
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the main application
    try:
        from src.main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
