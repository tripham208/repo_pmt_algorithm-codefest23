from typing import Any

from gst import PLAYER_ID
from gst.algorithm.minimax import val, MIN, check_pos_can_go
from gst.handler.map_handler import NO_LIST, MAP
from gst.model.const import get_action_in_zone
from copy import deepcopy

from gst.model.position import Position

COUNT = 0

H_NOE = 4  # dộ sâu


def minimax_no_e(position: Position, zone: int) -> list:
    value = MIN
    # print(position)
    pos_list = [position.pos_player]
    act_list = []

    try:
        actions = get_action_in_zone(zone)
        print(actions)

        for act in actions:
            match act:
                case [1, 1]:
                    print(f"action:{act} level:0 ")
                    if not position.bomb_player:
                        continue
                    new_position = deepcopy(position)
                    new_position.bomb_player = False

                    new_position.bombs = deepcopy(position.bombs)
                    new_position.bombs.append(
                        {
                            "row": new_position.pos_player[0],
                            "col": new_position.pos_player[1],
                            "playerId": PLAYER_ID
                        }
                    )

                    # print(new_position)
                    new_act_list = deepcopy(act_list)
                    new_act_list.append(act)
                    new_pos_list = deepcopy(pos_list)
                    point, pos, move = max_val_no_e(new_position, actions, 1, new_pos_list, new_act_list)
                    if value < point:
                        print(f"61 action:{act} level:{0} -{point, pos, move} yes")
                        value = point
                        act_list = move
                        pos_list = pos
                case [0, 0]:
                    point = val(position=position)
                    if value < point:
                        print(f"61 action:{act} level:{0} -{point} yes")
                        value = point
                        act_list.append(act)
                case _:
                    # reposition
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                    print(f"67 action:{act} level:{0}")

                    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                        continue
                    if not check_pos_can_go(new_pos_player, position):
                        continue
                    new_position = deepcopy(position)
                    new_position.pos_player = new_pos_player
                    # bên trên đã thay đổi nên dưới dugn lại bị sai
                    new_pos_list = deepcopy([position.pos_player])
                    new_act_list = deepcopy([])
                    new_act_list.append(act)
                    point, pos, move = max_val_no_e(new_position, actions, 1, new_pos_list, new_act_list)
                    if value < point:
                        print(f"75 action:{act} level:{0} point: {point}  {move} yes")
                        value = point
                        act_list = move
                        pos_list = pos

    finally:
        pass
    return act_list


def max_val_no_e(position: Position, actions, level, pos_list: list, act_list) -> tuple[
    Any, list[Any] | Any, list[Any] | Any]:
    value = MIN
    move = []
    pos = []
    # check_kill()
    try:
        for act in actions:
            match act:
                case [1, 1]:
                    if level <= 2:
                        print(f"100 {act_list} action:{act} level:{level} ")
                        point, pos_l, move_l = bomb_action(position=position, actions=actions, level=level,
                                                           list_pos=pos_list,
                                                           list_move=act_list)
                        if value < point:
                            value = point
                            move = move_l
                            pos = pos_l
                    print("105 - end act", move, "point:", value, "level", level)
                case [0, 0]:
                    print(f"110 {act_list} action:{act}, val: {value} level:{level} ")
                    point = val(position)
                    if value < point:
                        value = point
                        new_pos_list = deepcopy(pos_list)
                        new_move_list = deepcopy(act_list)
                        new_move_list.append(act)
                        move = new_move_list
                        pos = new_pos_list
                    print("115 - move end", move, "point:", val(position=position), "level", level)
                case _:
                    # reposition
                    print(f"120 {act_list} action:{act} level:{level} ")
                    point, pos_l, move_l = move_action(position=position, current_action=act, actions=actions,
                                                       level=level,
                                                       pos_list=pos_list, move_list=act_list)

                    if value < point:
                        print(f"125 action:{act} level:{level} point: {point} {pos_l} {move_l}")
                        value = point
                        move = move_l
                        pos = pos_l
                    print("130 - end act", move, "point:", value, "level", level)

        return value, pos, move
    finally:
        return value, pos, move


def bomb_action(position: Position, actions, level, list_pos, list_move):
    if not position.bomb_player:
        return MIN, list_pos, list_move
    new_position = deepcopy(position)
    new_position.bomb_player = False
    new_position.bombs = deepcopy(position.bombs)
    new_position.bombs.append(
        {
            "row": new_position.pos_player[0],
            "col": new_position.pos_player[1],
            "playerId": PLAYER_ID
        }
    )

    new_pos_list = deepcopy(list_pos)
    new_move_list = deepcopy(list_move)
    new_move_list.append([1, 1])

    if level != H_NOE:
        print(level, "bomb")
        return max_val_no_e(position=new_position, actions=actions, level=level + 1, pos_list=new_pos_list,
                            act_list=new_move_list)
    else:
        print("End ", list_pos)
        return MIN, new_pos_list, new_move_list


def move_action(position: Position, current_action, actions, level, pos_list, move_list):
    if level != H_NOE and current_action == [0, 0]:
        return MIN, pos_list, move_list
    new_pos_player = [sum(i) for i in zip(position.pos_player, current_action)]

    if not check_pos_can_go(new_pos_player, position):
        return MIN, pos_list, move_list
    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
        return MIN, pos_list, move_list
    if new_pos_player in pos_list:  # list check đã đi qua
        return MIN, pos_list, move_list
    print("170", move_list, "moving", current_action)
    new_position = deepcopy(position)
    new_position.pos_player = new_pos_player
    new_pos_list = deepcopy(pos_list)
    new_pos_list.append(new_pos_player)
    new_move_list = deepcopy(move_list)
    new_move_list.append(current_action)

    if level != H_NOE:
        # print("moved ", current_action)
        return max_val_no_e(position=new_position, actions=actions, level=level + 1, pos_list=new_pos_list,
                            act_list=new_move_list)
    else:
        print("185 - move end", new_move_list, "point:", val(position=new_position), "level", level)
        return val(position=new_position), new_pos_list, new_move_list
