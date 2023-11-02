from copy import deepcopy
from typing import Any

import socketio

from gst.handler import show_map
from gst.model.const import NextMoveZone, BombRange, get_move_in_zone, get_action_in_zone
import math as m

from gst.model.position import Position
# global var
URL = 'http://localhost:1543/'
GAME_ID = "eeec3b93-24e7-4d78-94e1-65846b0381c8"
PLAYER_ID = "player1-xxx"
ENEMY_ID = "player2-xxx"

JOIN_GAME_EVENT = 'join game'
TICKTACK_EVENT = "ticktack player"
DRIVE_EVENT = "drive player"
DELAY_FRAME_TIME = 4

sio = socketio.Client()

# map handler

MAP_DEFAULT = []

MAP = []
EVALUATE_MAP_PLAYER = []
EVALUATE_MAP_ENEMY = []
EVALUATE_MAP_ROAD = []
COLS = 0
ROWS = 0

POS_PLAYER = []  # [5, 10]  # row - col
POS_ENEMY = []  # [5, 15]

POS_PLAYER_EGG = []  # row - col
POS_ENEMY_EGG = []

BOMB_PLAYER_ENABLE = False
BOMB_ENEMY_ENABLE = False
BOMB_DANGER_POS = []
BOMBS = []
SPOILS = []
SPOILS_POS = []
EF_PLAYER = {
    "power": 1,
    "lives": 1000
}
EF_ENEMY = {
    "power": 1,
    "lives": 3
}

NO_LIST = [1, 2, 3, 5, 11, 16]

NO_DESTROY_LIST = [1, 3]
"""
0 - A Road \n
1 - A Wall (None destructible cell)\n
2 - A Balk (Destructible cell)\n
3 - A Teleport Gate\n
4 - A Quarantine Place \n
5 - A Dragon Egg GST\n

11 - Bomb \n
16 - Mystic egg - change in set spoil
"""

NO_LIST_M = [1, 2, 3, 11]
"""
0 - A Road \n
1 - A Wall (None destructible cell)\n
2 - A Balk (Destructible cell)\n
3 - A Teleport Gate\n
4 - A Quarantine Place \n
5 - A Dragon Egg GST\n

11 - Bomb \n
"""

ZONE_CLEAN = [0, 0, 0, 0]


#
#
#

def paste_base_map(data):
    """
    first handle ticktack \n
    - map size
    - map
    - data player
    - point map

    """
    global COLS
    global ROWS
    global MAP
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_PLAYER
    COLS = data["map_info"]["size"]["cols"]
    ROWS = data["map_info"]["size"]["rows"]
    MAP = data["map_info"]["map"]
    paste_gst_egg(eggs=data["map_info"]["dragonEggGSTArray"])
    paste_player_data(players=data["map_info"]["players"])
    # EVALUATE_MAP_PLAYER = data["map_info"]["map"]
    # EVALUATE_MAP_ENEMY = data["map_info"]["map"]
    # print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)
    reset_point_map()
    replace_point_map()


def paste_gst_egg(eggs):
    global POS_PLAYER_EGG
    global POS_ENEMY_EGG
    for egg in eggs:
        if egg["id"] == PLAYER_ID:
            POS_PLAYER_EGG = [egg["row"], egg["col"]]
        else:
            POS_ENEMY_EGG = [egg["row"], egg["col"]]


def paste_player_data(players):
    global POS_PLAYER
    global POS_ENEMY
    global EF_PLAYER
    global EF_ENEMY
    for player in players:
        if player["id"] == PLAYER_ID:
            POS_PLAYER = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
            EF_PLAYER["power"] = player["power"]
            if player["lives"] == EF_PLAYER["lives"] - 1:
                print(
                    f"------------------{player['lives']}----------------------{EF_PLAYER['lives'] - 1}---------------")
            EF_PLAYER["lives"] = player["lives"]
        else:
            POS_ENEMY = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
            EF_ENEMY["power"] = player["power"]
            EF_ENEMY["lives"] = player["lives"]


def paste_update_map(data):
    """
    handler update ticktack \n
    - list bomb
    - list spoil
    - data player
    - point map
    - map

    """

    global MAP
    global BOMBS
    global SPOILS
    global BOMB_DANGER_POS

    global COLS
    global ROWS
    COLS = data["map_info"]["size"]["cols"]
    ROWS = data["map_info"]["size"]["rows"]

    BOMBS = data["map_info"]["bombs"]
    # BOMB_DANGER_POS = get_list_pos_bomb_danger(BOMBS)
    SPOILS = data["map_info"]["spoils"]
    paste_player_data(players=data["map_info"]["players"])
    paste_gst_egg(eggs=data["map_info"]["dragonEggGSTArray"])
    # tee()
    MAP = data["map_info"]["map"]
    reset_point_map()
    # show_map(EVALUATE_MAP_ROAD)
    # show_map(EVALUATE_MAP_PLAYER)
    replace_point_map()

    # show_map(EVALUATE_MAP_ROAD)
    # show_map(EVALUATE_MAP_PLAYER)


def set_spoil():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_ROAD
    global SPOILS_POS
    SPOILS_POS = []
    for spoil in SPOILS:
        if spoil["spoil_type"] in [3, 4, 5]:  # type egg can use
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = 200
            EVALUATE_MAP_ENEMY[spoil["row"]][spoil["col"]] = -200
            EVALUATE_MAP_ROAD[spoil["row"]][spoil["col"]] += 50
            SPOILS_POS.append([spoil["row"], spoil["col"]])
            for i in BombRange.LV1.value:  # ko phải bomb nổ :  khoảng cách  =1
                # a.append([EVALUATE_MAP_ROAD[row + i[0]][col + i[1]], i])
                EVALUATE_MAP_ROAD[spoil["row"] + i[0]][spoil["col"] + i[1]] += 50
        else:
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = -200
            # MAP[spoil["row"]][spoil["col"]] = 16  # lock map


def set_bomb():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    for bomb in BOMBS:
        if bomb["playerId"] == PLAYER_ID:
            set_bomb_point(EF_PLAYER["power"], bomb)
        else:
            set_bomb_point(EF_ENEMY["power"], bomb)


def set_bomb_point(power, bomb):
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_ROAD
    global MAP

    MAP[bomb["row"]][bomb["col"]] = 11  # lock map
    EVALUATE_MAP_PLAYER[bomb["row"]][bomb["col"]] = -500
    EVALUATE_MAP_ROAD[bomb["row"]][bomb["col"]] = -500
    EVALUATE_MAP_ENEMY[bomb["row"]][bomb["col"]] = 500

    # todo :handle time
    # handle bomb bị tường chặn => done
    match power:
        case 1:
            for i in BombRange.LV1.value:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ROAD[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 2:
            bomb_point_with_lv(bomb, BombRange.LV2.value)
        case 3:
            bomb_point_with_lv(bomb, BombRange.LV3.value)


def bomb_point_with_lv(bomb, bomb_range) -> int:
    value = 0
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                continue
            else:
                EVALUATE_MAP_PLAYER[bomb["row"] + j[0]][bomb["col"] + j[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + j[0]][bomb["col"] + j[1]] = 500
                EVALUATE_MAP_ROAD[bomb["row"] + j[0]][bomb["col"] + j[1]] = -500
    return value


def replace_point_map():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global BOMBS
    for row in range(ROWS):
        for col in range(COLS):
            if MAP[row][col] == 2:
                # a = [[row, col], MAP[row][col], EVALUATE_MAP_ROAD[row][col]]
                # show_map(EVALUATE_MAP_ROAD)
                for i in BombRange.LV1.value:  # ko phải bomb nổ :  khoảng cách  =1
                    # a.append([EVALUATE_MAP_ROAD[row + i[0]][col + i[1]], i])
                    EVALUATE_MAP_ROAD[row + i[0]][col + i[1]] += 25
                    # a.append([row + i[0], col + i[1], EVALUATE_MAP_ROAD[row + i[0]][col + i[1]]])
                # print(a)
                '''
                # only map change update point todo: check this
                # map change khi có gỗ bị phá vậy thì có cần up date point ko?
                if MAP[row][col] == current_map[row][col]:
                    pass
                else:
                    EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                    EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])'''
    # show_map(EVALUATE_MAP_ROAD)

    set_addition_point()


def create_map_zero():
    l = []
    row = [0] * COLS
    for i in range(ROWS):
        l.append(deepcopy(row))

    return l


def reset_point_map():
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ROAD
    a = create_map_zero()
    EVALUATE_MAP_PLAYER = deepcopy(a)
    EVALUATE_MAP_ENEMY = deepcopy(a)
    EVALUATE_MAP_ROAD = deepcopy(a)


def set_addition_point():
    set_bomb()
    set_spoil()


# socket handler


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.on(event=JOIN_GAME_EVENT)
def event_handle(data):
    print(f"joined game:{data}")


@sio.on(event=TICKTACK_EVENT)
def event_handle(data):
    ticktack_handler(data)


@sio.on(event=DRIVE_EVENT)
def event_handle(data):
    if data["player_id"] is ENEMY_ID:
        print(f"drive:{data}")


def connect_server():
    sio.connect(URL)


def emit_event(event: str, arg):
    sio.emit(event=event, data=arg)


def join_game(game_id: str, player_id: str):
    emit_event(JOIN_GAME_EVENT, {
        "game_id": game_id,
        "player_id": player_id
    })


def emit_direction(direction):
    emit_event(DRIVE_EVENT, {
        "direction": direction
    })


def ticktack_handler(data):
    global BOMB_DANGER_POS
    print(data["id"], "-", data["tag"])

    BOMB_DANGER_POS = get_list_pos_bomb_danger(data["map_info"]["bombs"])  # update liên tục
    """
    #update theo tag
    match data["tag"]:
        case "bomb:explosed":
            BOMB_DANGER_POS = get_list_pos_bomb_danger(data["map_info"]["bombs"])
        case "bomb:setup":
            BOMB_DANGER_POS = get_list_pos_bomb_danger(data["map_info"]["bombs"])"""
    # print(BOMB_DANGER_POS)
    match data["id"]:
        case 1:
            paste_base_map(data)
        case x if x % DELAY_FRAME_TIME == 0:
            paste_update_map(data)

            print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)
            action_case = get_case_action()

            action = get_action(case=action_case)
            print(action_case, action)
            if action_case == 2 and action == []:
                print("find egg")
                action = get_action(case=5)
            print("action:", action)
            direction = gen_direction(action)
            print("direction:", direction)

            emit_direction(direction)


def get_case_action() -> int:
    if True:  # is_save_zone():
        # show_map(EVALUATE_MAP_ROAD)
        # show_map(EVALUATE_MAP_PLAYER)
        val_pos = EVALUATE_MAP_ROAD[POS_PLAYER[0]][POS_PLAYER[1]]
        print("pos", POS_PLAYER, "point :", val_pos)
        if val_pos != 0:
            return 1
        elif val_pos == 0:
            return 2
    else:
        return 3
    return 1


# action handler

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
    global BOMB_PLAYER_ENABLE
    global BOMB_ENEMY_ENABLE

    size = [ROWS, COLS]
    zone = is_zone(POS_PLAYER, size)
    p, e = get_status_bomb()
    BOMB_PLAYER_ENABLE, BOMB_ENEMY_ENABLE = p, e

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
            """
            return minimax_ab(
                position=Position(
                    pos_player=POS_PLAYER,
                    pos_enemy=POS_ENEMY,
                    bomb_player=p,
                    bomb_enemy=e,
                    bombs=BOMBS
                )
            )"""

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


# algorithm
# init

def euclid_distance(a: list, b: list):
    return m.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def is_zone(pos: list, size: list) -> int:
    """

    :param pos:
    :param size:
    :return: zone     1,2 /3,4
    """
    p1 = m.floor(size[0] / 2)
    p2 = m.floor(size[1] / 2)

    if pos[0] < p1:
        if pos[1] < p2:
            return 1
        else:
            return 2
    else:
        if pos[1] < p2:
            return 3
        else:
            return 4


def check_half_zone(p_zone, e_zone):
    """
    1: nưa tren
    2: nưa dươi
    3: nưa trai
    4: nưa phai
    :return: hz player,hz enemy
    """
    if p_zone in [1, 3] and e_zone in [2, 4]:
        return 3, 4
    elif p_zone in [2, 4] and e_zone in [1, 3]:
        return 4, 3
    elif p_zone in [1, 2] and e_zone in [3, 4]:
        return 1, 2
    elif p_zone in [3, 4] and e_zone in [1, 2]:
        return 2, 1
    else:
        return 0, 0


def is_save_zone():
    global POS_PLAYER
    # print(POS_PLAYER)
    # zp = is_zone(POS_PLAYER, [ROWS, COLS])
    # ze = is_zone(POS_ENEMY, [ROWS, COLS])
    if euclid_distance(POS_ENEMY, POS_PLAYER) >= 4:
        return True
    else:
        return False


def is_odd(n) -> bool:
    return n % 2 == 1


def change_haft_zone(h_zone, e_zone):
    """

    :param h_zone:
    :param e_zone:
    :return: target zone
    """
    match [h_zone, e_zone]:
        case [1, 3]:
            return 4
        case [1, 4]:
            return 1
        case [2, 3]:
            return 3


# todo : check zone

def check_zone_clean_balk(size: list, zone):
    p1 = m.floor(size[0] / 2)
    p2 = m.floor(size[1] / 2)
    match zone:
        case 1:
            for i in range(p1):
                for j in range(p2):
                    if MAP[i][j] == 2:
                        return False
        case 2:
            for i in range(p1):
                for j in range(p2, size[1]):
                    if MAP[i][j] == 2:
                        return False
        case 3:
            for i in range(p1, size[p1]):
                for j in range(p2):
                    if MAP[i][j] == 2:
                        return False
        case 4:
            for i in range(p1, size[p1]):
                for j in range(p2, size[1]):
                    if MAP[i][j] == 2:
                        return False
    return True


# a star

def a_star(start, target):
    # print(start, target)
    queue = [[start, euclid_distance(start, target), [start], []]]  # pos , dis, pos_list, act_list
    lock_list = [start]  # lọc lặp

    while queue:
        cr_status = queue.pop(0)
        # print(cr_status)
        if cr_status[0] == target:
            return cr_status[3]
        for act in NextMoveZone.Z4.value:
            new_pos_player = [sum(i) for i in zip(cr_status[0], act)]
            if new_pos_player in BOMB_DANGER_POS:
                continue

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


# bfs


def bfs(start: list, size_map: list, p_zone: int, e_zone: int, hz=None):
    pos_list = [start]  # lọc lặp
    actions = get_move_in_zone(p_zone)
    if hz is None:
        hz, _ = check_half_zone(p_zone, e_zone)
    # print("hz", hz)
    queue = []
    act_list = []
    try:
        begin_status = [start, []]  # current pos , action to pos

        point, pos_list, end_status = next_pos_bfs(actions, begin_status, pos_list, size_map, hz, e_zone, queue)
        print("685", point, pos_list, end_status)
        if point >= 25:
            # print("return", end_status[1])
            act_list = end_status[1]
    finally:
        return act_list[0:4]


def next_pos_bfs(actions, cr_status, pos_list, size_map, hz, e_zone, queue: list):
    for act in actions:
        new_pos_player = [sum(i) for i in zip(cr_status[0], act)]
        #print("line 700", cr_status, "->", new_pos_player)
        if new_pos_player in pos_list:
            continue
        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
            # print("wall")
            continue
        if new_pos_player in BOMB_DANGER_POS:
            continue

        z, _ = check_half_zone(is_zone(cr_status[0], [ROWS, COLS]), e_zone)
        pz, ez = is_zone(cr_status[0], [ROWS, COLS]), is_zone(POS_ENEMY, [ROWS, COLS])
        if pz == ez:
            continue

        # print(z, hz)
        # if hz != z:  # zone  block
        # print("out zone")
        # continue

        point = EVALUATE_MAP_ROAD[new_pos_player[0]][new_pos_player[1]]
        #print("line 715", cr_status, "->", new_pos_player, point, pos_list)
        if point >= 25 and new_pos_player not in BOMB_DANGER_POS:  # not is_danger_bombs(new_pos_player, BOMBS):
            end_status = deepcopy(cr_status)
            end_status[1].append(act)
            end_status[0] = new_pos_player
            pos_list.append(new_pos_player)
            # print("705", point, pos_list, end_status)
            return point, pos_list, end_status
        # print("710")
        new_status = deepcopy(cr_status)
        new_status[1].append(act)
        new_status[0] = new_pos_player

        pos_list.append(new_pos_player)
        queue.append(new_status)

    #print("line 730", queue)

    next_status = queue.pop(0)

    point, pos_list, end_status = next_pos_bfs(actions, next_status, pos_list, size_map, hz, e_zone, queue)

    return point, pos_list, end_status


# minimax
# init

COUNT = 0
MAX = 10000000
MIN = -10000000
LOSE = -10000
WIN = 10000
TMP_MAX = 1000
TMP_MIN = -1000
P1 = 1  # player
P2 = 2  # enemy


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


def bomb_bonus(bomb) -> int:
    if bomb["playerId"] == PLAYER_ID:
        return destroy_point(EF_PLAYER["power"], bomb)
    else:
        return destroy_point(EF_ENEMY["power"], bomb)


def destroy_point(power, bomb) -> int:
    point = 0
    match power:
        case 1:
            for i in BombRange.LV1.value:
                if MAP[bomb["row"] + i[0]][bomb["col"] + i[1]] == 2:
                    point += 100
        case 2:
            point += destroy_point_with_lv(bomb, BombRange.LV2.value)
        case _:
            point += destroy_point_with_lv(bomb, BombRange.LV3.value)
    return point


def destroy_point_with_lv(bomb, bomb_range) -> int:
    value = 0
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 2:
                value += 100
    return value


def list_pos_bomb(power, bomb) -> list:
    list_pos = [[bomb["row"], bomb["col"]]]
    print("835 : add list bomb pos")
    match power:
        case 1:
            for i in BombRange.LV1.value:
                # print([bomb["row"] + i[0], bomb["col"] + i[1]], position)
                list_pos.append([bomb["row"] + i[0], bomb["col"] + i[1]])
        case 2:
            list_pos += list_pos_bomb_with_lv(bomb, BombRange.LV2.value)
        case _:
            list_pos += list_pos_bomb_with_lv(bomb, BombRange.LV3.value)
    return list_pos


def list_pos_bomb_with_lv(bomb, bomb_range) -> list:
    list_pos = []
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:  # todo check lại vụ cản xem đúng chưa
                continue

            list_pos.append([bomb["row"] + j[0], bomb["col"] + j[1]])
    return list_pos


def get_list_pos_bomb_danger(bombs):
    list_pos = []
    for bomb in bombs:
        print("870", bomb)
        if bomb["remainTime"] > 1300:
            continue
        if bomb["playerId"] == PLAYER_ID:
            list_pos += list_pos_bomb(EF_PLAYER["power"], bomb)
        else:
            list_pos += list_pos_bomb(EF_ENEMY["power"], bomb)
    return list_pos


def is_danger_bombs(position, bombs) -> bool:
    """

    :param position:
    :param bombs: [{col,row,playerId}]
    :return:
    """
    # print("check danger", position, bombs)
    for bomb in bombs:
        if bomb["playerId"] == PLAYER_ID:
            return is_pos_danger(EF_PLAYER["power"], bomb, position)
        else:
            return is_pos_danger(EF_ENEMY["power"], bomb, position)


def is_danger_bomb(position, bomb) -> bool:
    """

    :param position:
    :param bomb: {col,row,playerId}
    :return:
    """
    # print("check danger", position, bombs)
    if bomb["playerId"] == PLAYER_ID:
        return is_pos_danger(EF_PLAYER["power"], bomb, position)
    else:
        return is_pos_danger(EF_ENEMY["power"], bomb, position)


def is_pos_danger(power, bomb, position):
    if [bomb["row"], bomb["col"]] == position:
        return True
    match power:
        case 1:
            for i in BombRange.LV1.value:
                # print([bomb["row"] + i[0], bomb["col"] + i[1]], position)
                if [bomb["row"] + i[0], bomb["col"] + i[1]] == position:
                    return True
        case 2:
            return is_pos_danger_with_lv(bomb, BombRange.LV2.value, position)
        case _:
            return is_pos_danger_with_lv(bomb, BombRange.LV3.value, position)
    return False


def is_pos_danger_with_lv(bomb, bomb_range, position) -> int:
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                continue
            if [bomb["row"] + j[0], bomb["col"] + j[1]] == position:
                return True
    return False


def val(position: Position, list_pos=None) -> int:
    """
    val  =  val map(+road) + bonus point (bomb nổ trúng thùng / địch)
    :return:
    """
    value = sum(
        [
            EVALUATE_MAP_PLAYER[position.pos_player[0]][position.pos_player[1]],
            EVALUATE_MAP_ROAD[position.pos_player[0]][position.pos_player[1]],
            EVALUATE_MAP_ENEMY[position.pos_enemy[0]][position.pos_enemy[1]]
        ]
    )
    # print("check val")

    global COUNT
    COUNT = COUNT + 1
    # print("count", COUNT, position)
    if position.bombs:
        for bomb in position.bombs:
            if is_danger_bomb(position.pos_player, bomb):
                value -= 1000
            if is_danger_bomb(position.pos_enemy, bomb):
                value += 100
            if bomb["playerId"] == PLAYER_ID:
                value += bomb_bonus(bomb) * 1.5
            else:
                value -= bomb_bonus(bomb)
    else:
        pass
    if list_pos is not None:
        for i in list_pos:
            if i in SPOILS_POS:
                value += 100
    return value


def check_pos_can_go(new_pos, position: Position):
    list_pos = [position.pos_enemy]
    for bomb in position.bombs:
        list_pos.append([bomb["row"], bomb["col"]])
    if new_pos in list_pos:
        return False
    return True


# ab

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
    # print(beta, level, "end")
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


# NOE

H_NOE = 3  # dộ sâu


def minimax_no_e(position: Position, zone: int) -> list:
    value = MIN
    # print(position)
    pos_list = [position.pos_player]
    act_list = []

    try:
        actions = get_action_in_zone(zone)
        # print(actions)

        for act in actions:
            match act:
                case [1, 1]:
                    print(f"{act_list} action:{act} level:0 ")
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
                    new_act_list = deepcopy([])
                    new_act_list.append(act)
                    new_pos_list = deepcopy(pos_list)
                    point_no_e, pos, move = max_val_no_e(new_position, actions, 1, new_pos_list, new_act_list)
                    if value < point_no_e:
                        # print(f"1160 action:{act} level:{0} -{point_no_e, pos, move} yes")
                        value = point_no_e
                        act_list = move
                        pos_list = pos
                case [0, 0]:
                    point_no_e = val(position=position)
                    if value < point_no_e:
                        # print(f"1170 action:{act} level:{0} -{point_no_e} yes")
                        value = point_no_e
                        act_list = [act]
                case _:
                    # reposition
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                    # print(f"1175 action:{act} level:{0}")
                    if BOMB_PLAYER_ENABLE and new_pos_player in BOMB_DANGER_POS:
                        continue
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
                    point_no_e, pos, move = max_val_no_e(new_position, actions, 1, new_pos_list, new_act_list)
                    if value < point_no_e:
                        # print(f"1190 action:{act} level:{0} point: {point_no_e}  {move} yes")
                        value = point_no_e
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
                    if level <= (H_NOE - 2):
                        # print(f"1210 {act_list} action:{act} level:{level} ")
                        point_max_no_e, pos_l, move_l = bomb_action(position=position, actions=actions, level=level,
                                                                    list_pos=pos_list,
                                                                    list_move=act_list)
                        if value < point_max_no_e:
                            value = point_max_no_e
                            move = move_l
                            pos = pos_l
                    # print("1215 - end act", move, "point:", value, "level", level)
                case [0, 0]:
                    # print(f"1220 {act_list} action:{act}, val: {value} level:{level} ")
                    point_max_no_e = val(position)
                    # print(point_max_no_e)
                    if value < point_max_no_e:
                        value = point_max_no_e
                        new_pos_list = deepcopy(pos_list)
                        new_move_list = deepcopy(act_list)
                        new_move_list.append(act)
                        move = new_move_list
                        pos = new_pos_list
                    # print("1225 - move end", move, "point:", val(position=position), "level", level)
                case _:
                    # reposition
                    # print(f"1230 {act_list} action:{act} level:{level} ")
                    point_max_no_e, pos_l, move_l = move_action(position=position, current_action=act, actions=actions,
                                                                level=level,
                                                                pos_list=pos_list, move_list=act_list)

                    if value < point_max_no_e:
                        # print(f"1235 action:{act} level:{level} point: {point_max_no_e} {pos_l} {move_l}")
                        value = point_max_no_e
                        move = move_l
                        pos = pos_l
                    # print("1240 - end act", move, "point:", value, "level", level)

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
        # print(level, "bomb")
        return max_val_no_e(position=new_position, actions=actions, level=level + 1, pos_list=new_pos_list,
                            act_list=new_move_list)
    else:
        # print("End ", list_pos)
        return MIN, new_pos_list, new_move_list


def move_action(position: Position, current_action, actions, level, pos_list, move_list):
    if level != H_NOE and current_action == [0, 0]:
        return MIN, pos_list, move_list
    new_pos_player = [sum(i) for i in zip(position.pos_player, current_action)]
    if new_pos_player in BOMB_DANGER_POS:  # and BOMB_PLAYER_ENABLE
        return MIN, pos_list, move_list
    """
    if level >= 2 and new_pos_player in BOMB_DANGER_POS:
        return MIN, pos_list, move_list
    """
    if not check_pos_can_go(new_pos_player, position):
        return MIN, pos_list, move_list
    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST:
        return MIN, pos_list, move_list
    if new_pos_player in pos_list:  # list check đã đi qua
        return MIN, pos_list, move_list
    # print("170", move_list, "moving", current_action)
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
        # print("185 - move end", new_move_list, "point:", val(position=new_position), "level", level)
        return val(position=new_position), new_pos_list, new_move_list


if __name__ == '__main__':
    connect_server()
    join_game(
        game_id=GAME_ID,
        player_id=PLAYER_ID
    )
