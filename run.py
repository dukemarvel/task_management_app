import signal
import uvicorn
from backend.main import app

def signal_handler(sig, frame):
    print("Signal received, shutting down...")
    uvicorn.Server.should_exit = True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    uvicorn.run(app, host="192.168.43.199", port=5000)
