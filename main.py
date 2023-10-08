from gst.algorithm.a_star.a_star import a_star
from gst.algorithm.fs.bfs import bfs
from gst.algorithm.fs.dfs import dfs
from gst.algorithm.minimax.minimax_a2 import minimax
from gst.algorithm.minimax.minimax_ab import minimax_ab
from gst.algorithm.minimax.minimax_no_e import minimax_no_e
from gst.handler.action_handler import gen_direction
from gst.handler.map_handler import *
from gst.model.position import Position

direction = []

s = [8, 2]


def sa():
    match s:
        case [5, 2]:
            print(False)
        case [x, 2] if x > 7:
            print(False, "d")
        case [_, 2]:
            print(True)
        case _:
            print("uk")


if __name__ == '__main__':
    mock_default()
    match 1:
        case 1:
            a = minimax_no_e(position=Position(
                pos_player=POS_PLAYER,
                pos_enemy=POS_ENEMY,
                bomb_player=True,
                bomb_enemy=True
            ), zone=1)
        case 2:
            a = minimax_ab(position=Position(
                pos_player=POS_PLAYER,
                pos_enemy=POS_ENEMY,
                bomb_player=True,
                bomb_enemy=True
            ))
        case 3:
            a = bfs(POS_PLAYER, [ROWS, COLS], 1, 2)

    print("g:", gen_direction([a]))
    print("g:", gen_direction(a))
    print("g:", a)

    # b = bfs(POS_PLAYER, [ROWS, COLS], 1, 2)
    # print(b)

    # print(a_star(POS_PLAYER, [11, 23]))
