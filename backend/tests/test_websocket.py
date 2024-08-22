import pytest
from fastapi.testclient import TestClient
from backend.main import app
from fastapi import WebSocketDisconnect

client = TestClient(app)

def test_websocket_chat():
    user_id = 1
    with client.websocket_connect(f"/ws/chat/{user_id}") as websocket:
        # Send a message through the WebSocket
        message = "Hello, World!"
        websocket.send_text(message)
        
        # Receive the broadcasted message
        received = websocket.receive_text()
        assert received == f"User {user_id} says: {message}"

def test_websocket_disconnect():
    user_id = 2
    with client.websocket_connect(f"/ws/chat/{user_id}") as websocket:
        message = "Disconnecting..."
        websocket.send_text(message)
        
        # Simulate disconnection
        websocket.close()
        
        # Attempt to send a message after disconnect (should raise an exception)
        try:
            websocket.send_text("This should not go through")
        except Exception as e:
            assert isinstance(e, WebSocketDisconnect)
