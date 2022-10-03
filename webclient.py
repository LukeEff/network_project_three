import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])

# Create connection
s = socket.socket()
destination = (host, port)
s.connect(destination)

# Send request
req = 'GET //Users/luke/PycharmProjects/network_project_three/file1.txt HTTP/1.1\r\n\
Host: {}\r\n\
Connection: close\r\n\
\r\n'.format(host).encode("ISO-8859-1")
s.sendall(req)

# Receive response
response = s.recv(4096)
while len(response) > 0:
    print(response.decode("ISO-8859-1"))
    response = s.recv(4096)

# Close connection
print("Finished receiving response. Closing connection")
s.close()
