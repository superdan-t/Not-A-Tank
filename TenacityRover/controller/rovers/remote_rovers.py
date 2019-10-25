from . import rover_network


class RoverIDError(Exception):
    pass


class RoverConnectError(Exception):
    pass


class RemoteRover(object):
    def __init__(self, i2d):
        self.id = i2d
        self.status = 'UNINITIALIZED'
        self.connected = False

        self.net = rover_network.RNet(self)

    def check_id(self):
        """Throws exceptions if there is a problem with the ID"""
        prob = self.problems_with_id()
        if prob == 'NONE':
            return
        else:
            raise RoverIDError(prob)

    def id_valid(self):
        """Boolean check whether the ID is valid"""
        if self.problems_with_id() == 'NONE':
            return True
        else:
            return False

    def problems_with_id(self):
        """Find problems in IDs"""
        if 8 <= len(self.id) <= 12:
            allowed_special_chars = "!@#*%&"
            for char in self.id:
                char_b = char.encode('utf-8')[0]
                if not (65 <= char_b <= 90 or 97 <= char_b <= 122 or 48 <= char_b <= 57):
                    if allowed_special_chars.find(char) == -1:
                        return 'BAD_SPECIAL'
            return 'NONE'
        elif not 8 <= len(self.id):
            if self.id == '':
                return 'EMPTY'
            return 'SHORT'
        else:
            return 'LONG'

    def retrieve_details(self):
        self.check_id()
        self.status, self.net.rov_address = self.net.get_details()

    def connect(self):
        self.check_id()
        if self.net.enable_connection_mode() == 'ACCEPT':
            self.retrieve_details()
            if self.status == 'VANISHED':
                raise RoverConnectError('Specified rover is offline.')
            self.connected = self.net.linked()

    def disconnect(self):
        self.check_id()
        self.connected = False
        self.net.get_response(self.net.rov_address, 'TERMINATE')
