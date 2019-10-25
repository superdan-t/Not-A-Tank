import socket
import threading
from server import rov_manager
from server import ref

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_port = 16505
socket_hostname = ref.hostname


def start_server(hostname=socket_hostname, port=socket_port):
    try:
        global socket_port, socket_hostname
        socket_port = port
        socket_hostname = hostname
        print('Starting server with hostname ' + hostname + ' on the port ' + str(port))
        server_socket.bind((hostname, port))
        server_socket.listen(5)
        x = threading.Thread(target=handle_connections, daemon=True)
        x.start()
    except OSError as e:
        if len(e.args) > 0 and type(e.args[0]) == int and e.args[0] == 10048:
            print('Couldn\'t start the server because the port is busy. Maybe another service is using it or you tried'
                  ' to start multiple instances of this server. Run command "restart" to try again.')


def change_properties(hostname=socket_hostname, port=socket_port):
    global socket_port, socket_hostname, server_socket
    socket_port = port
    socket_hostname = hostname
    print('Applying any changes to server...')
    server_socket.close()
    server_socket.detach()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)


def handle_connections():
    while True:
        try:
            (client_socket, address) = server_socket.accept()

            data = client_socket.recv(1024)

            for request in data.decode("utf-8").split(' '):

                identity = request.split('=')

                if len(identity) > 1:
                    if identity[0] == 'ROV.PING.ID':
                        rov_manager.status_received_from_tank(identity[1], address[0], address[1])
                    elif identity[0] == 'DETAILS.ID':
                        target = rov_manager.get_tank(identity[1])
                        if type(target) == bool and not target:
                            client_socket.send(('ID=' + identity[1] + ' STATUS=VANISHED').encode('utf-8'))
                        else:
                            client_socket.send(target.dump_details().encode('utf-8'))
                    elif identity[0] == 'INFO':
                        client_socket.send(('TYPE=ROVSTAT VERSION=' + ref.version).encode('utf-8'))

            client_socket.close()
        except OSError as e:
            if e.errno == 10038 or e.errno == 10022:
                pass
            else:
                raise e
