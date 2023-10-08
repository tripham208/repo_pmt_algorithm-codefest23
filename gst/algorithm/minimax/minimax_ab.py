from gst import PLAYER_ID, ENEMY_ID
from gst.algorithm.minimax import P2, val, P1, MIN, MAX, check_pos_can_go
from gst.handler.map_handler import NO_LIST, MAP
from copy import deepcopy

from gst.model.position import Position

COUNT = 0

H_AB = 5  # dộ sâu

ACTIONS_AB = [[1, 1], [0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]]
"""
0-1
2-3
4-5
"""


def minimax_ab(position: Position) -> list:
    alpha = MIN
    beta = MAX
    action = None
    try:
        for act in ACTIONS_AB:
            match act:
                case [1, 1]:
                    # print(f"action:{act} level:0")
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
                    point = min_val(new_position, 1, player=P2, alpha=alpha, beta=beta)
                    if alpha < point:
                        # print(f"61 action:{act} level: 0 :{alpha} -> {point}yes")
                        alpha = point
                        action = act
                case [0, 0]:
                    continue
                case _:
                    # reposition
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                    # print(f"67 action:{act} level:{0}")
                    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                        continue
                    if not check_pos_can_go(new_pos_player, position):
                        continue
                    new_position = deepcopy(position)
                    new_position.pos_player = new_pos_player

                    point = min_val(new_position, 1, player=P2, alpha=alpha, beta=beta)
                    if alpha < point:
                        # print(f"75 action:{act} level:0 -:{alpha} -> {point} yes")
                        alpha = point
                        action = act
    finally:
        pass
    # print(action)
    return [action]


def min_val(position: Position, level, player, alpha, beta) -> int:
    # check_kill()
    # print(position)
    # print([level, player], "min")
    if level == H_AB:
        # print(f"match [{H}, 2]")
        try:
            for act in ACTIONS_AB:
                match act:
                    case [1, 1]:
                        if not position.bomb_enemy:
                            continue
                        new_position = deepcopy(position)
                        new_position.bomb_enemy = False
                        # print(f"p: {player} action:{act} level:{level}")
                        new_position.bombs = deepcopy(position.bombs)
                        new_position.bombs.append(
                            {
                                "row": new_position.pos_enemy[0],
                                "col": new_position.pos_enemy[1],
                                "playerId": ENEMY_ID
                            }
                        )

                        point = val(position=new_position)
                        if beta > point:
                            beta = point
                            # print(new_position, "=>", point)
                            if alpha > beta:
                                break
                    case _:
                        # reposition
                        new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]
                        if not check_pos_can_go(new_pos_enemy, position):
                            continue
                        if MAP[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                            continue
                        # print(f"p: {player} action:{act} level:{level}")
                        new_position = deepcopy(position)
                        new_position.pos_enemy = new_pos_enemy

                        point = val(position=new_position)
                        if beta > point:
                            beta = point
                            # print(new_position, "=>", point)
                        if alpha > beta:
                            break
        finally:
            pass
    else:
        try:
            for act in ACTIONS_AB:
                match act:
                    case [1, 1]:
                        # print(f"p: {player} action:{act} level:{level}")
                        if not position.bomb_enemy:
                            continue
                        new_position = deepcopy(position)
                        new_position.bomb_enemy = False
                        # print(f"224 action:{act} level:{level}")
                        new_position.bombs = deepcopy(position.bombs)
                        new_position.bombs.append(
                            {
                                "row": new_position.pos_enemy[0],
                                "col": new_position.pos_enemy[1],
                                "playerId": ENEMY_ID
                            }
                        )

                        point = max_val(position=new_position, level=level + 1, player=P1, alpha=alpha, beta=beta)
                        # print(f"234 action:{act} level:{level} value:{beta} point:{point}")
                        if beta > point:
                            beta = point
                            if alpha > beta:
                                break
                    case [0, 0]:
                        continue
                    case _:
                        # reposition
                        new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]
                        # print(f"p: {player} action:{act} level:{level}")
                        if MAP[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                            continue
                        if not check_pos_can_go(new_pos_enemy, position):
                            continue
                        new_position = deepcopy(position)
                        new_position.pos_enemy = new_pos_enemy

                        point = max_val(position=new_position, level=level + 1, player=P1, alpha=alpha, beta=beta)
                        # print(f"249 action:{act} level:{level} value:{beta} point:{point}")
                        if beta > point:
                            beta = point
                            if alpha > beta:
                                break
        finally:
            pass
    ##print(beta, level, "end")
    return beta


def max_val(position: Position, level, player, alpha, beta) -> int:
    # check_kill()
    # print(position)
    # print([level, player])
    if level == H_AB:
        try:
            for act in ACTIONS_AB:
                match act:
                    case [1, 1]:
                        pass
                    case _:
                        # reposition
                        new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                        if not check_pos_can_go(new_pos_player, position):
                            continue
                        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                            continue
                        # print(f"p: {player} action:{act} level:{level}")
                        new_position = deepcopy(position)
                        new_position.pos_player = new_pos_player

                        point = val(position=new_position)
                        if alpha < point:
                            alpha = point
                            # print(new_position, "=>", point)
                            if alpha > beta:
                                break
        finally:
            pass

    else:
        try:
            for act in ACTIONS_AB:
                match act:
                    case [1, 1]:
                        if not position.bomb_player:
                            continue
                        new_position = deepcopy(position)
                        new_position.bomb_player = False
                        # print(f"p: {player} action:{act} level:{level}")
                        new_position.bombs = deepcopy(position.bombs)
                        new_position.bombs.append(
                            {
                                "row": new_position.pos_player[0],
                                "col": new_position.pos_player[1],
                                "playerId": PLAYER_ID
                            }
                        )

                        point = min_val(position=new_position, level=level + 1, player=P2, alpha=alpha, beta=beta)
                        if alpha < point:
                            alpha = point
                            # print(new_position, "=>", point)
                    case [0, 0]:
                        continue
                    case _:
                        # reposition
                        new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                        if not check_pos_can_go(new_pos_player, position):
                            continue
                        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                            continue
                        # print(f"p: {player} action:{act} level:{level}")
                        new_position = deepcopy(position)
                        new_position.pos_player = new_pos_player

                        point = min_val(position=new_position, level=level + 1, player=P2, alpha=alpha, beta=beta)
                        if alpha < point:
                            alpha = point
                            # print(alpha)
                            if alpha > beta:
                                break
        finally:
            pass
    # print(alpha, level, "end")
    return alpha
