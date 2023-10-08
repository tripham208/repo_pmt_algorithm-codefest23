from copy import deepcopy

from gst.algorithm import is_zone, check_half_zone
from gst.algorithm.minimax import is_danger
from gst.handler.map_handler import MAP, NO_LIST, EVALUATE_MAP_ROAD, POS_ENEMY, ROWS, COLS, BOMBS
from gst.model.const import get_move_in_zone


# dfs

def bfs(start: list, size_map: list, p_zone: int, e_zone: int, hz=None):
    pos_list = [start]  # lọc lặp
    actions = get_move_in_zone(p_zone)
    if hz is None:
        hz, _ = check_half_zone(p_zone, e_zone)
    queue = []
    act_list = []
    try:
        begin_status = [start, []]  # current pos , action to pos

        point, pos_list, end_status = next_pos_bfs(actions, begin_status, pos_list, size_map, hz, e_zone, queue)
        # print("23", point, pos_list, end_status)
        if point >= 25:
            # print("return")
            act_list = end_status[1]
    finally:
        return act_list


def next_pos_bfs(actions, cr_status, pos_list, size_map, hz, e_zone, queue: list):
    for act in actions:
        new_pos_player = [sum(i) for i in zip(cr_status[0], act)]

        if new_pos_player in pos_list:
            continue
        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
            # print("wall")
            continue

        z, _ = check_half_zone(is_zone(cr_status[0], [ROWS, COLS]), e_zone)
        # print(z, hz)
        if hz != z:  # zone  block
            # print("out zone")
            continue

        point = EVALUATE_MAP_ROAD[new_pos_player[0]][new_pos_player[1]]
        # print("29", cr_status, "->", new_pos_player, point, pos_list)
        if point >= 25 and is_danger(new_pos_player, BOMBS):
            end_status = deepcopy(cr_status)
            end_status[1].append(act)
            end_status[0] = new_pos_player
            pos_list.append(new_pos_player)
            return point, pos_list, end_status

        new_status = deepcopy(cr_status)
        new_status[1].append(act)
        new_status[0] = new_pos_player

        pos_list.append(new_pos_player)
        queue.append(new_status)

    # print(queue)

    next_status = queue.pop(0)

    point, pos_list, end_status = next_pos_bfs(actions, next_status, pos_list, size_map, hz, e_zone, queue)

    return point, pos_list, end_status
