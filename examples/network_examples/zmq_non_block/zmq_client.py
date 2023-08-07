import zmq

context = zmq.Context()

print("Connecting to the server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Set the socket to non-blocking mode
socket.setsockopt(zmq.RCVTIMEO, 0)  # Timeout for receive in milliseconds (1 second)

for request_number in range(5):
    message = f"Request #{request_number}".encode('utf-8')
    print(f"Sending: {message}")
    socket.send(message)

    # Wait for the reply from the server, handle non-blocking mode
    try:
        reply = socket.recv()

        print(f"Received reply: {reply.decode('utf-8')}")
    except zmq.Again:
        print("No reply received yet.")


print("Requester (client) exiting.")
