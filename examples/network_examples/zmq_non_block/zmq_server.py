import zmq

context = zmq.Context()

print("Starting the server...")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Set the socket to non-blocking mode
socket.setsockopt(zmq.RCVTIMEO, 1000)  # Timeout for receive in milliseconds (1 second)

while True:
    # Wait for the request from the client, handle non-blocking mode
    try:
        request = socket.recv()
        print(f"Received request: {request.decode('utf-8')}")

        # Simulate some processing
        import time
        time.sleep(1)

        # Send the reply back to the client
        reply_message = "Reply to " + request.decode('utf-8')
        socket.send(reply_message.encode('utf-8'))
    except zmq.Again:
        print("No request received yet, continuing other tasks...")
