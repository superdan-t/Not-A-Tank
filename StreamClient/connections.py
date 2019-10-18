import socket
import ref

class ConnectionDeniedError(Exception):
    pass


class RemoteRover:
    def __init__(self, uid):
        self.location = ('', 0)
        self.connected = False
        self.id = uid
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 'UNKNOWN'

    def get_status(self):
        status, ip, port = '', '', ''
        try:
            status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            status_socket.connect(ref.rovstat_serv)
            status_socket.send(('DETAILS.ID=' + self.id).encode(ref.encoding))
            response = status_socket.recv(256).decode(ref.encoding)

            response = response.split(' ')

            for query in response:
                var_name, val = query.split('=', 1)
                if var_name == 'STATUS':
                    status = val
                elif var_name == 'IP':
                    ip = val
                elif var_name == 'PORT':
                    port = int(val)
        except (socket.gaierror, socket.timeout):
            pass

        self.location = (ip, port)
        self.status = status
        return status, ip, port

    def enable_connections(self):
        """Tell the rover to listen to this device through the rovstat server"""
        try:
            self.s.connect(ref.rovstat_serv)
            self.s.send(('LISTEN.ID=' + self.id))
            response = self.s.recv(256).decode(ref.encoding)
            if response == 'LISTEN.DENY':
                raise ConnectionDeniedError
        except (socket.gaierror, socket.timeout):
            pass

    def disconnect(self):
        self.s.connect(self.location)
        self.s.send(b'DISCONNECT.SENDER')
        self.connected = False

    def connect(self):
        """Establish our connection"""
        self.get_status()
        if self.status == 'ACTIVE':
            try:
                self.enable_connections()
                self.s.connect(self.location)
                self.s.send(b'CONNECT.SENDER')
                response = self.s.recv(256).decode(ref.encoding)
                if response == 'CONNECT.DENY':
                    self.connected = False
                elif response == 'CONNECT.APPROVE':
                    self.connected = True
            except (socket.gaierror, socket.timeout, ConnectionDeniedError):
                self.connected = False
        else:
            self.connected = False
