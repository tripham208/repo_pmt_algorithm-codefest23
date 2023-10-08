from gst import PLAYER_ID
from gst.algorithm import is_zone
from gst.algorithm.a_star.a_star import a_star
from gst.algorithm.fs.bfs import bfs
from gst.algorithm.minimax.minimax_ab import minimax_ab
from gst.algorithm.minimax.minimax_no_e import minimax_no_e
from gst.handler.map_handler import POS_PLAYER, ROWS, COLS, POS_ENEMY, BOMBS, POS_ENEMY_EGG, POS_PLAYER_EGG

from gst.model.position import Position


def gen_direction(direction):
    """
    1 - Move LEFT \n
    2 - Move RIGHT.\n
    3 - Move UP\n
    4 - Move DOWN\n
    b - Drop BOMB\n
    x - Stop Moving\n
    :param direction:
    :return:
    """
    output = ""
    for i in direction:
        match i:
            case [0, -1]:
                output += '1'
            case [0, 1]:
                output += '2'
            case [-1, 0]:
                output += '3'
            case [1, 0]:
                output += '4'
            case [0, 0]:
                output += 'x'
            case [1, 1]:
                output += 'b'
    return output


def get_status_bomb():
    p = True
    e = True
    for bomb in BOMBS:
        if bomb["playerId"] == PLAYER_ID:
            p = False
        else:
            e = False
    return p, e


def get_action(case) -> list:
    """
    1 -> action no e (road point >=25) \n
    2 -> find pos bomb \n
    3 -> action ab
    5 -> find egg enemy
    6 -> find egg player
    :param case:
    :return:
    """
    size = [ROWS, COLS]
    zone = is_zone(POS_PLAYER, size)
    p, e = get_status_bomb()
    match case:
        case 1:
            return minimax_no_e(
                position=Position(
                    pos_player=POS_PLAYER,
                    pos_enemy=POS_ENEMY,
                    bomb_player=p,
                    bomb_enemy=e,
                    bombs=BOMBS
                ),
                zone=zone
            )
        case 2:
            return bfs(
                start=POS_PLAYER,
                size_map=[ROWS, COLS],
                p_zone=is_zone(pos=POS_PLAYER, size=size),
                e_zone=is_zone(pos=POS_ENEMY, size=size)
            )
        case 3:
            return minimax_ab(
                position=Position(
                    pos_player=POS_PLAYER,
                    pos_enemy=POS_ENEMY,
                    bomb_player=p,
                    bomb_enemy=e,
                    bombs=BOMBS
                )
            )
        case 5:
            return a_star(
                start=POS_PLAYER,
                target=POS_ENEMY_EGG
            )
        case 6:
            return a_star(
                start=POS_PLAYER,
                target=POS_PLAYER_EGG
            )
