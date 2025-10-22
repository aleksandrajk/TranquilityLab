from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher
import threading
import time

class OSCManager:
    def __init__(self, send_ip='127.0.0.1', send_port=8000, receive_port=8001):
        self.send_ip = send_ip
        self.send_port = send_port
        self.receive_port = receive_port
        
        # OSC client for sending data to TouchDesigner
        self.client = udp_client.SimpleUDPClient(send_ip, send_port)
        
        # OSC server for receiving data from TouchDesigner
        self.dispatcher = Dispatcher()
        self.setup_handlers()
        
        self.server = osc_server.ThreadingOSCUDPServer(
            (send_ip, receive_port), self.dispatcher
        )
        
        self.received_data = {}
        
    def setup_handlers(self):
        """Setup OSC message handlers"""
        def default_handler(address, *args):
            self.received_data[address] = args
            print(f"Received OSC: {address} {args}")
            
        self.dispatcher.set_default_handler(default_handler)
        
    def start_receiver(self):
        """Start OSC receiver in a separate thread"""
        def run_server():
            print(f"OSC Receiver started on port {self.receive_port}")
            self.server.serve_forever()
            
        receiver_thread = threading.Thread(target=run_server, daemon=True)
        receiver_thread.start()
        
    def send_message(self, address, value):
        """Send OSC message to TouchDesigner"""
        try:
            self.client.send_message(address, value)
        except Exception as e:
            print(f"Error sending OSC: {e}")
            
    def get_parameter(self, address, default=None):
        """Get received parameter value"""
        return self.received_data.get(address, [default])[0]

if __name__ == "__main__":
    # Test OSC manager
    osc_mgr = OSCManager()
    osc_mgr.start_receiver()
    
    # Test sending some messages
    for i in range(5):
        osc_mgr.send_message("/test/value", i * 0.2)
        time.sleep(0.5)
