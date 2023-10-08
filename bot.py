from copy import deepcopy

from gst import GAME_ID, PLAYER_ID
from gst.handler.socket_handler import connect_server, join_game

if __name__ == '__main__':
    a = True
    b = a
    a= False
    print(b,a)
