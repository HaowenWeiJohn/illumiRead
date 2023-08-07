import zmq

context = zmq.Context()

print("Connecting to the server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Send a request and wait for a reply
for request_number in range(5):
    message = f"Request #{request_number}".encode('utf-8')
    print(f"Sending: {message}")
    socket.send(message)

    # Wait for the reply from the server
    reply = socket.recv()
    print(f"Received reply: {reply.decode('utf-8')}")

print("Requester (client) exiting.")
