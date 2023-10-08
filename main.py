from copy import deepcopy

from gst.handler.map_handler import *
from gst.minimax import Position, minimax

direction = []

s = [1, 1]


def sa():
    match s:
        case [1, 2]:
            print(False)
        case [_, 1]:
            print(True)
        case _:
            print("uk")


if __name__ == '__main__':
    mock_default()
    a = minimax(current_map=MAP,
                position=Position(
                    pos_player=POS_PLAYER,
                    pos_enemy=POS_ENEMY,
                    bomb_player=True,
                    bomb_enemy=True
                ), level=0)
    print(a)
    print(MAP[5][15])