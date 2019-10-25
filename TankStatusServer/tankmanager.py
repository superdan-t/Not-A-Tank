import time
import threading

active_tanks = []


class Tank:
    def __init__(self, unique_id, ip_address, port):
        self.update_time = time.time()
        self.id = unique_id
        self.ip_addr = ip_address
        self.port = port
        self.status = 'ACTIVE'

    def check_activity(self):
        if 10 >= time.time() - self.update_time > 25:
            self.status = 'SILENT'
        elif time.time() - self.update_time > 60:
            self.status = 'VANISHED'
        else:
            self.status = 'ACTIVE'

    def dump_details(self, verbose=False):
        if not verbose:
            return 'ID=' + self.id + ' IP=' + str(self.ip_addr) + ' PORT=' + str(self.port) + ' STATUS=' + self.status


def status_received_from_tank(unique_id, ip, port):
    for tank in active_tanks:
        if tank.id == unique_id:
            tank.update_time = time.time()
            tank.ip_addr = ip
            tank.port = port
            return
    active_tanks.append(Tank(unique_id, ip, port))
    print('A new tank connected with details ', end='')
    print(active_tanks[len(active_tanks) - 1].dump_details())


def remove_inactive_tanks():
    for tank in active_tanks:
        tank.check_activity()
        if tank.status == 'VANISHED':
            active_tanks.remove(tank)


def begin_tank_checking():
    x = threading.Thread(target=update_tanks_thread, daemon=True)
    x.start()


def update_tanks_thread():
    while True:
        remove_inactive_tanks()


def get_tank(unique_id):
    for tank in active_tanks:
        if tank.id == unique_id:
            return tank
    return False
