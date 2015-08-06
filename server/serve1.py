import socket as s

HOST, PORT = '', 8888

''' 
 s.AF_INET     : Address family for IPv4 internet protocols
 s.SOCK_STREAM : Used for TCP
 s.SOL_SOCKET  : Protocol level 
 s.SO_REUSEADDR: Allows us to reuse our source address and port for the dest

 The listen method takes a backlog, which is the limit
 for the queue of incoming connections. 
'''

listen_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
listen_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print('Serving HTTP on port {0}'.format(PORT))

while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        print(request.decode('utf-8'))

        http_response = '''\
HTTP/1.1 200 OK

Hello, World!
'''
        client_connection.sendall(bytes(http_response))
        client_connection.close()
