from copy import deepcopy

from gst.algorithm import is_zone, check_half_zone
from gst.handler.map_handler import MAP, NO_LIST, EVALUATE_MAP_ROAD, POS_ENEMY, ROWS, COLS
from gst.model.const import get_move_in_zone


# dfs

def dfs(start: list, size_map: list, p_zone: int, e_zone: int):
    pos_list = [start]
    act_list = []
    actions = get_move_in_zone(p_zone)
    hz, _ = check_half_zone(p_zone, e_zone)
    try:

        point, pos, move = next_pos_dfs(actions, start, pos_list, act_list, size_map, hz, e_zone)
        print("23", point, pos, move)
        if point >= 25:
            print("return")
            act_list = move
    finally:
        return act_list


def next_pos_dfs(actions, cr_pos, pos_list, act_list, size_map, hz, e_zone):
    point = EVALUATE_MAP_ROAD[cr_pos[0]][cr_pos[1]]
    print("29", point, cr_pos, pos_list, act_list)
    if point >= 25:
        return point, pos_list, act_list
    else:
        for act in actions:
            new_pos_player = [sum(i) for i in zip(cr_pos, act)]
            print(point, cr_pos, new_pos_player)
            if new_pos_player in pos_list:
                continue
            if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                print("wall")
                continue

            z, _ = check_half_zone(is_zone(cr_pos, [ROWS, COLS]), e_zone)
            print(z, hz)
            if hz != z:  # zone  block
                print("out zone")
                continue

            new_pos_list = deepcopy(pos_list)
            new_pos_list.append(new_pos_player)
            new_act_list = deepcopy(act_list)
            new_act_list.append(act)
            print("45", cr_pos, new_pos_player, new_pos_list, new_act_list)
            point, pos, move = next_pos_dfs(actions, new_pos_player, new_pos_list, new_act_list, size_map, hz, e_zone)

            print("55", point, pos, move)
            if point >= 25:
                return point, pos, move
