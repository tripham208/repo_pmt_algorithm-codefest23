from gst import PLAYER_ID, ENEMY_ID
from gst.handler.map_handler import NO_LIST, BOMBS, EF_PLAYER, EF_ENEMY, EVALUATE_MAP_ENEMY, EVALUATE_MAP_PLAYER, LV1, \
    LV2, LV3
from copy import deepcopy

MAX = 10000000
MIN = -10000000
LOSE = -10000
WIN = 10000
TMP_MAX = 1000
TMP_MIN = -1000
H = 3  # dộ sâu
P1 = 1  # player
P2 = 2  # enemy
ACTIONS = [[1, 1], [0, -1], [1, 0], [0, 1], [-1, 0], [0, 0]]


class Position:
    def __init__(self,
                 pos_player: list,
                 pos_enemy: list,
                 bomb_player: bool,
                 bomb_enemy: bool,
                 bombs=None
                 ):
        if bombs is None:
            bombs = []
        self.bombs = bombs  # bomb hiện tại
        self.bomb_enemy = bomb_enemy
        self.bomb_player = bomb_player
        self.pos_player = pos_player
        self.pos_enemy = pos_enemy


def minimax(current_map, level, position: Position) -> list:
    value = MIN
    action = None
    try:
        for act in ACTIONS:
            map2 = deepcopy(current_map)  # todo: move after check
            match act:
                case [1, 1]:
                    if not position.bomb_player:
                        continue
                    new_position = deepcopy(position)
                    new_position.bomb_player = False

                    new_position.bombs = deepcopy(BOMBS).append(
                        {
                            "row": new_position.pos_player[0],
                            "col": new_position.pos_player[1],
                            "playerId": PLAYER_ID
                        }
                    )

                    if value < min_val(position, map2, level + 1, player=P2):
                        action = act

                case _:
                    # reposition
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                    if current_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                        continue

                    new_position = deepcopy(position)
                    new_position.pos_player = new_pos_player

                    if value < min_val(position, map2, level + 1, player=P2):
                        action = act
    finally:
        pass

    return action


def min_val(position: Position, cr_map, level, player, h=H) -> int:
    value = MAX
    # check_kill()
    match [level, player]:
        case [h, 1]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = val(cr_map=map2, position=new_position)
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = val(cr_map=map2, position=new_position)
                            if value > point:
                                value = point
                return value
            finally:
                pass
        case [h, 2]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": ENEMY_ID
                                }
                            )

                            point = val(cr_map=map2, position=new_position)
                            if value > point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = val(cr_map=map2, position=new_position)
                            if value > point:
                                value = point
                return value
            finally:
                pass
        case [_, 1]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = max_val(cr_map=map2, position=new_position, level=level + 1, player=P2)
                            if value >= point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = max_val(cr_map=map2, position=new_position, level=level + 1, player=P2)
                            if value >= point:
                                value = point
                return value
            finally:
                pass
        case [_, 2]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": ENEMY_ID
                                }
                            )

                            point = max_val(cr_map=map2, position=new_position, level=level + 1, player=P1)
                            if value >= point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = max_val(cr_map=map2, position=new_position, level=level + 1, player=P1)
                            if value >= point:
                                value = point
                return value
            finally:
                pass
    return value


def max_val(position: Position, cr_map, level, player, h=H) -> int:
    value = MIN
    # check_kill()
    match [level, player]:
        case [h, 1]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = val(cr_map=map2, position=new_position)
                            if value < point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = val(cr_map=map2, position=new_position)
                            if value < point:
                                value = point
                return value
            finally:
                pass
        case [h, 2]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": ENEMY_ID
                                }
                            )

                            point = val(cr_map=map2, position=new_position)
                            if value < point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = val(cr_map=map2, position=new_position)
                            if value < point:
                                value = point
                return value
            finally:
                pass
        case [_, 1]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_player:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_player = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_player[0],
                                    "col": new_position.pos_player[1],
                                    "playerId": PLAYER_ID
                                }
                            )

                            point = min_val(cr_map=map2, position=new_position, level=level + 1, player=P2)
                            if value >= point:
                                value = point

                        case _:
                            # reposition
                            new_pos_player = [sum(i) for i in zip(position.pos_player, act)]

                            if cr_map[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_player = new_pos_player

                            point = min_val(cr_map=map2, position=new_position, level=level + 1, player=P2)
                            if value <= point:
                                value = point
                return value
            finally:
                pass
        case [_, 2]:
            try:
                for act in ACTIONS:
                    map2 = deepcopy(cr_map)  # todo: move after check
                    match act:
                        case [1, 1]:
                            if not position.bomb_enemy:
                                continue
                            new_position = deepcopy(position)
                            new_position.bomb_enemy = False

                            new_position.bombs = deepcopy(BOMBS).append(
                                {
                                    "row": new_position.pos_enemy[0],
                                    "col": new_position.pos_enemy[1],
                                    "playerId": ENEMY_ID
                                }
                            )

                            point = min_val(cr_map=map2, position=new_position, level=level + 1, player=P1)
                            if value <= point:
                                value = point

                        case _:
                            # reposition
                            new_pos_enemy = [sum(i) for i in zip(position.pos_enemy, act)]

                            if cr_map[new_pos_enemy[0]][new_pos_enemy[1]] in NO_LIST:
                                continue

                            new_position = deepcopy(position)
                            new_position.pos_enemy = new_pos_enemy

                            point = min_val(cr_map=map2, position=new_position, level=level + 1, player=P1)
                            if value <= point:
                                value = point
                return value
            finally:
                pass
    return value


def check_kill() -> int:
    if EF_PLAYER["lives"] == 0:
        return LOSE
    elif EF_ENEMY["lives"] == 0:
        return WIN
    return 0


def check_kill_v2(player, lives) -> int:
    if [player, lives] == [P1, 0]:
        return LOSE
    elif [player, lives] == [P2, 0]:
        return WIN
    return 0


def bomb_bonus(bomb, cr_map) -> int:
    if bomb["playerId"] == PLAYER_ID:
        return destroy_point(EF_PLAYER["power"], bomb, cr_map)
    else:
        return destroy_point(EF_ENEMY["power"], bomb, cr_map)


def destroy_point(power, bomb, cr_map) -> int:
    point = 0
    match power:
        case 1:
            for i in LV1:
                if cr_map[bomb["row"] + i[0]][bomb["col"] + i[1]] == 2:
                    point += 100
        case 2:
            for i in LV2:
                if cr_map[bomb["row"] + i[0]][bomb["col"] + i[1]] == 2:
                    point += 100
        case 3:
            for i in LV3:
                if cr_map[bomb["row"] + i[0]][bomb["col"] + i[1]] == 2:
                    point += 100
    return point


def is_danger(position, bomb) -> bool:
    """

    :param position:
    :param bomb: {col,row,playerId}
    :return:
    """
    if bomb["playerId"] == PLAYER_ID:
        return is_pos_danger(EF_PLAYER["power"], bomb, position)
    else:
        return is_pos_danger(EF_ENEMY["power"], bomb, position)


def is_pos_danger(power, bomb, position):
    match power:
        case 1:
            for i in LV1:
                if [bomb["row"] + i[0]][bomb["col"] + i[1]] == position:
                    return True
        case 2:
            for i in LV2:
                if [bomb["row"] + i[0]][bomb["col"] + i[1]] == position:
                    return True
        case 3:
            for i in LV3:
                if [bomb["row"] + i[0]][bomb["col"] + i[1]] == position:
                    return True


def val(cr_map, position: Position) -> int:
    """
    val  =  val map + bonus point (bomb nổ trúng thùng / địch)
    :return:
    """
    value = 0
    value += EVALUATE_MAP_PLAYER[position.pos_player[0]][position.pos_player[1]]
    value += EVALUATE_MAP_ENEMY[position.pos_enemy[0]][position.pos_enemy[1]]
    if position.bombs:
        for bomb in position.bombs:
            if is_danger(position.pos_player, bomb):
                value -= 100
            if is_danger(position.pos_enemy, bomb):
                value += 100
            if bomb["playerId"] == PLAYER_ID:
                value += bomb_bonus(bomb, cr_map)
            else:
                value -= bomb_bonus(bomb, cr_map)
    else:
        pass
    return value

# todo: val function handle bomb + point replace point from map
# todo: handle move mul step
#
#
