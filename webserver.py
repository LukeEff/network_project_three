import socket
import sys
import os

port = int(sys.argv[1])

# Create a connection
s = socket.socket()
s.bind(('', port))
s.listen()

extension_mapping = {'.txt': 'text/plain', '.ico': 'image/x-icon', '.html': 'text/html'}


def get_req(message_socket):
    encoded_req = message_socket.recv(4096)
    request = ""
    while True:
        decoded_req = encoded_req.decode("ISO-8859-1")
        request = request + decoded_req
        if decoded_req.find('\r\n\r\n'):
            print(request)
            return request
        encoded_req = message_socket.recv(4096)


while True:
    new_conn = s.accept()
    print(new_conn)
    new_socket = new_conn[0]
    req = get_req(new_socket)

    # Parse request
    parsed_req = req.split('\r\n')
    request_method = parsed_req[0].split()[0]
    request_path = parsed_req[0].split()[1]
    request_protocol = parsed_req[0].split()[2]
    file_path_tuple = os.path.split(request_path)
    file_name = file_path_tuple[1]
    file_extension_tuple = os.path.splitext(file_name)
    file_extension = file_extension_tuple[1]

    try:
        with open(file_name) as fp:
            data = fp.read()  # Read entire file
            data_len = data.encode("ISO-8859-1")
            content_length = len(data_len)

            resp = 'HTTP/1.1 200 OK\r\n\
            Content-Type: {}\r\n\
            Content-Length: {}\r\n\
            Connection: close\r\n\r\n\
            {}'.format(extension_mapping[file_extension], content_length, data).encode("ISO-8859-1")
            new_socket.sendall(resp)
    except:
        resp = 'HTTP/1.1 404 Not Found\r\n\
        Content-Type: {}\r\n\
        Content-Length: 13\r\n\
        Connection: close\r\n\r\n\
        404 not found'.format(extension_mapping[file_extension]).encode("ISO-8859-1")
        new_socket.sendall(resp)

    print("Found end of line. Closing new socket")
    new_socket.close()
