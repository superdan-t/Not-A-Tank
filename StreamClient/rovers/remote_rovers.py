from rovers import *


class RoverNoIdError(Exception):
    pass


class RemoteRover(object):
    def __init__(self, i2d):
        self.id = i2d
        self.status = 'UNINITIALIZED'
        self.connected = False

        self.net = RNet(self)

    def check_id_validity(self):
        if 8 <= len(self.id) <= 12:
            allowed_special_chars = "!@#*%&"
            for char in self.id:
                char_b = char.encode('utf-8')
                if not (65 <= char_b <= 90 and 97 <= char_b <= 122 and 48 <= char_b <= 57):
                    if allowed_special_chars.find(char) == -1:
                        return False
            return True
        else:
            return False

    def retrieve_details(self):
        if id == '':
            raise RoverNoIdError
        self.status, self.net.rov_address = self.net.get_details()

    def connect(self):
        if id == '':
            raise RoverNoIdError
        if self.net.enable_connection_mode() == 'ACCEPT':
            self.retrieve_details()
            self.connected = self.net.linked()

    def disconnect(self):
        if id == '':
            raise RoverNoIdError
        self.connected = False
        self.net.get_response(self.net.rov_address, 'TERMINATE')
