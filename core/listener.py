import threading
import time
import socket as sock
from PyQt6.QtCore import QObject, pyqtSignal
# Added import for proper type annotation of signals
from PyQt6.QtCore import pyqtBoundSignal


class ConnectionListener(QObject):
    """Listens for incoming connection requests"""
    
    # Signal emitted when a connection request is received
    connection_received: pyqtBoundSignal = pyqtSignal(str)
    
    # Type annotations for class attributes
    is_listening: bool
    listener_thread: threading.Thread | None
    socket: sock.socket | None
    
    def __init__(self):
        super().__init__()
        self.is_listening = False
        self.listener_thread = None
        self.socket = None
        
    def start(self):
        """Start the listener"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.listener_thread = threading.Thread(target=self._listen, daemon=True)
        _ = self.listener_thread.start()
        
    def stop(self):
        """Stop the listener"""
        self.is_listening = False
        if self.socket:
            _ = self.socket.close()
        if self.listener_thread:
            _ = self.listener_thread.join()
            
    def _listen(self):
        """Listen for incoming connections (simulated)"""
        # In a real implementation, you would set up actual network listening
        # For demonstration, we'll simulate receiving connection requests
        counter = 1
        while self.is_listening:
            try:
                # Simulate receiving a connection request
                _ = time.sleep(5)  # Wait 5 seconds between requests
                if self.is_listening:
                    request_data = f"Connection request #{counter} at {time.ctime()}"
                    _ = self.connection_received.emit(request_data)
                    counter += 1
            except Exception as e:
                if self.is_listening:
                    print(f"Listener error: {e}")
                break