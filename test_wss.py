import websocket    # python -m pip install --user websocket-client

def test_websocket_connection():
    url = "wss://api-scarpiso.crtx.au.paloaltonetworks.com/xsoar/d1ws"

    try:
        ws = websocket.create_connection(url)
        print("WebSocket connection successful")
        ws.close()
    except Exception as e:
        print(f"WebSocket connection failed: {str(e)}")

if __name__ == "__main__":
    test_websocket_connection()
