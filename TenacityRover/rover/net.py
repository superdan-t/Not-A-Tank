"""Rover should use two sockets: one for controller connections, one for video stream"""

import socket
import random
from rover import ref

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
