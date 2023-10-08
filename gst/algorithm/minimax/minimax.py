from gst import PLAYER_ID
from gst.algorithm.minimax import P2, val, P1, MIN, MAX
from gst.handler.map_handler import NO_LIST
from copy import deepcopy

from gst.model.position import Position

COUNT = 0

H = 5  # dộ sâu

ACTIONS = [[1, 1], [0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]]


def minimax(current_map, position: Position) -> list:
    value = MIN
    action = None
    try:
        for act in ACTIONS:
            map2 = deepcopy(current_map)  # todo: move after check
            match act:
                case [1, 1]:
                    print(f"action:{act} level:0")
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

                    print(new_position)
                    point = min_val(new_position, map2, 1, player=P2)
                    if value < point:
                        print(f"61 action:{act} level: 0 -{value} yes")
                        value = point
                        action = act

                case _:
                    # reposition
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                    print(f"67 action:{act} level:{0}")
                    if current_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                        continue

                    new_position = deepcopy(position)
                    new_position.pos_player = new_pos_player

                    point = min_val(new_position, map2,  1, player=P2)
                    if value < point:
                        print(f"75 action:{act} level:0 -:{value} yes")
                        value = point
                        action = act
    finally:
        pass

    return action


def min_val(position: Position, cr_map, level, player, h=3) -> int:
    value = MAX
    # check_kill()
    print(position)
    print([level, player], h)
    match [level, player]:
        case [5, 1]:
            print("match [h, 1]")
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            print(f"action:{act} level:{level}")
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

                            point = val(position=new_position)
                            if value > point:
                                print(f"action:{act} level:{level} - yes")
                                value = point

                        case _:
                            # reposition
                            print(f"action:{act} level:{level}")
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player
                            print(f"action:{act} level:{level} - yes")
                            point = val(position=new_position)
                            if value > point:
                                value = point
                return value
            finally:
                pass
        case [5, 2]:
            print("match [h, 2]", h)
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:

                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = val(position=new_position)
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = val(position=new_position)
                            if value > point:
                                value = point
                return value
            finally:
                pass
        case [x, 2] if x > 4:
            map2 = deepcopy(cr_map)
            new_position = deepcopy(position)

            point = max_val(position=new_position, level=level + 1, player=P1)
            if value > point:
                value = point

        case [_, 1]:
            print("match [_, 1]")
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = max_val(position=new_position, level=level + 1, player=P2)
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = max_val(position=new_position, level=level + 1, player=P2)
                            if value > point:
                                value = point
                return value
            finally:
                pass
        case [_, 2]:
            print("match [_, 2] ...")
            try:
                for act in ACTIONS:
                    print(act)
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            print(f"220 action:{act} level:{level}")
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False
                            print(f"224 action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = max_val(position=new_position, level=level + 1, player=P1)
                            print(f"234 action:{act} level:{level} value:{value} point:{point}")
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]
                            print(f"241 action:{act} level:{level}")
                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = max_val(position=new_position, level=level + 1, player=P1)
                            print(f"249 action:{act} level:{level} value:{value} point:{point}")
                            if value > point:
                                value = point
                return value
            finally:
                pass
    return value


def max_val(position: Position, cr_map, level, player, h=H) -> int:
    value = MIN
    # check_kill()
    print(position)
    print([level, player])
    match [level, player]:
        case [5, 1]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = val(position=new_position)
                            if value < point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = val(position=new_position)
                            if value < point:
                                value = point
                                print(value)
                return value
            finally:
                pass
        case [5, 2]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = val(position=new_position)
                            if value < point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = val(position=new_position)
                            if value < point:
                                value = point
                                print(value)
                return value
            finally:
                pass
        case [x, 2] if x > 4:
            map2 = deepcopy(cr_map)
            new_position = deepcopy(position)

            point = max_val(position=new_position, level=level + 1, player=P1)
            if value > point:
                value = point
        case [_, 1]:
            print("max [_, 1]")
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = min_val(position=new_position, level=level + 1, player=P2)
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = min_val(position=new_position, level=level + 1, player=P2)
                            if value < point:
                                value = point
                                print(value)
                return value
            finally:
                pass
        case [_, 2]:
            print("max [_, 2]")
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False
                            print(f"action:{act} level:{level}")
                            new_position.bombs = deepcopy(position.bombs)
                            new_position.bombs.append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = min_val(position=new_position, level=level + 1, player=P1)
                            if value < point:
                                value = point
                                print(value)

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue
                            print(f"action:{act} level:{level}")
                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = min_val(position=new_position, level=level + 1, player=P1)
                            if value < point:
                                value = point
                                print(value)
                return value
            finally:
                pass
    return value
