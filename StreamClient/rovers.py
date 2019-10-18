import socket
import ref


class RoverNoIdError(Exception):
    pass


class RemoteRover(object):
    def __init__(self):
        self.id = ''
        self.status = 'UNINITIALIZED'
        self.net = RNet()
        self.connected = False

    def update_details(self):
        if id == '':
            raise RoverNoIdError
        self.status, self.net.rov_address = self.net.get_details(self.id)

    def connect(self):
        if id == '':
            raise RoverNoIdError
        if self.net.enable_connection_mode() == 'ACCEPT':
            self.update_details()
            self.connected = self.net.linked()

    def disconnect(self):
        if id == '':
            raise RoverNoIdError
        self.connected = False
        self.net.get_response(self.net.rov_address, 'TERMINATE')





class RNet(object):
    """Network handler specifically for a rover"""
    def __init__(self):
        self.rov_address = ('', 0)

    @staticmethod
    def get_response(socket_address, message, max_len=512):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(socket_address)
            s.send(message.encode(ref.encoding))
            response = s.recv(max_len).decode(ref.encoding)
            s.close()
            return response
        except (socket.gaierror, socket.timeout):
            return ''

    def linked(self):
        response = self.get_response(self.rov_address, 'CONNECT.STATE').split(' ')
        if response[0] == 'CONNECT.STATE':
            if response[1] == 'TRUE':
                return True
            else:
                return False

    def get_details(self, rov_id):
        response = self.get_response(ref.rovstat_serv, 'DETAILS.ID=' + rov_id).split(' ')
        status, ip, port = '', '', ''
        for query in response:
            var_name, val = query.split('=', 1)
            if var_name == 'STATUS':
                status = val
            elif var_name == 'IP':
                ip = val
            elif var_name == 'PORT':
                port = int(val)
        return status, (ip, port)

    def enable_connection_mode(self, rov_id):
        response = self.get_response(ref.rovstat_serv, 'LISTEN.ID=' + rov_id).split('=')
        if response[0] == 'DENY':
            return response[1]
        elif response[0] == 'ACCEPT':
            return 'ACCEPT'
        else:
            return 'ERROR'
