from copy import deepcopy

from gst.algorithm import euclid_distance
from gst.handler.map_handler import NO_LIST, MAP, NO_DESTROY_LIST
from gst.model.const import NextMoveZone


def a_star(start, target):
    queue = [[start, euclid_distance(start, target), [start], []]]
    lock_list = [start]  # lọc lặp

    while queue:
        cr_status = queue.pop(0)
        # print(cr_status)
        if cr_status[0] == target:
            return cr_status[2]
        for act in NextMoveZone.Z4.value:
            new_pos_player = [sum(i) for i in zip(cr_status[0], act)]

            if MAP[new_pos_player[0]][new_pos_player[1]] in NO_DESTROY_LIST:
                continue

            if new_pos_player in lock_list:
                continue
            lock_list.append(new_pos_player)

            new_status = deepcopy(cr_status)

            new_status[0] = new_pos_player
            new_status[1] = euclid_distance(new_pos_player, target)
            new_status[2].append(new_pos_player)
            new_status[3].append(act)

            # print(cr_status[0], "=>", new_pos_player)

            queue.append(new_status)

        queue.sort(key=lambda x: x[1])
        # print(len(queue), queue)
    else:
        return []
