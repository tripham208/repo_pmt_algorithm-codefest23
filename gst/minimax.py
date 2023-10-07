from gst.handler.map_handler import map_copy, NO_LIST

MAX = 10000000
MIN = -10000000

ACTIONS = [[1, 1], [0, -1], [1, 0], [0, 1], [-1, 0], [0, 0]]


def minimax(current_map, h, pos_player, pos_enemy) -> list:
    value = MIN
    action = None
    try:
        for act in ACTIONS:
            map2 = map_copy(current_map)
            match act:
                case [1, 1]:
                    pass
                case _:
                    new_pos = [pos_player[0] + act[0], pos_player[1] + act[1]]
                    if current_map[new_pos[0]][new_pos[1]] in NO_LIST:
                        continue
                    if value < min_val(new_pos, pos_enemy, map2, h + 1, 0):
                        action = act
    finally:
        return action


def min_val(pos_player, pos_enemy, next_map, h, player) -> int:
    pass


def max_val(pos_player, pos_enemy, next_map, h, player) -> int:
    pass


def val():
    """
    val  =  val map + bonus point (bomb nổ trúng thùng / địch)
    :return:
    """
    pass

# todo: val function handle bomb + point replace point from map
#
#
#
