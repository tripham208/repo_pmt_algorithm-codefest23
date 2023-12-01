from copy import deepcopy

import socketio

from gst.model.const import NextMoveZone, BombRange, get_move_in_zone, get_action_out_zone, get_move_out_zone, \
    AroundRange
import math as m

from gst.model.position import Position
from pmt.util import pr_yellow, pr_green, pr_red

# global var
URL = "http://localhost:1543/"  # 'http://192.168.0.101/'
GAME_ID = "8314308c-d3aa-49ed-b3db-4dc10aa190eb"

PLAYER_ID = "player2-xxx"
# PLAYER_ID = "player1-xxx"

# ENEMY_ID = "player=2-xxx"

JOIN_GAME_EVENT = 'join game'
TICKTACK_EVENT = "ticktack player"
DRIVE_EVENT = "drive player"

sio = socketio.Client()

# map handler
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

BOMB_PLAYER_DELAY = 0
BOMB_PLAYER_ENABLE = False
BOMB_ENEMY_ENABLE = False
BOMB_POS_LOCK_MINMAX = []
BOMB_POS_LOCK_BFS = []
BOMBS = []
BOMBS_ = []  # bomb sawp
BOMBS_L2 = []  # bomb sawp

SPOILS = []
SPOILS_POS = []
EF_PLAYER = {
    "power": 1,
    "lives": 1000,
    "dragonEggDelay": 0,
}
EF_ENEMY = {
    "power": 1,
    "lives": 3
}

NO_LIST_MAX = [1, 2, 5, 11]

NO_LIST_BFS = [1, 2, 3, 5, 11]

NO_DESTROY_LIST = [1, 3, 5]
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
GAME_REMAIN_TIME = 0


#
#
#

def paste_gst_egg(eggs):
    global POS_PLAYER_EGG
    global POS_ENEMY_EGG
    for egg in eggs:
        if egg["id"] in PLAYER_ID:
            POS_PLAYER_EGG = [egg["row"], egg["col"]]
        else:
            POS_ENEMY_EGG = [egg["row"], egg["col"]]


def paste_player_data(players):
    global POS_PLAYER
    global POS_ENEMY
    global EF_PLAYER
    global EF_ENEMY
    global BOMB_PLAYER_DELAY
    for player in players:
        if player["id"] in PLAYER_ID:
            POS_PLAYER = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
            EF_PLAYER["power"] = player["power"]
            EF_PLAYER["dragonEggDelay"] = player["dragonEggDelay"]
            if player["lives"] == EF_PLAYER["lives"] - 1:
                print(
                    f"------------------{player['lives']}----------------------{EF_PLAYER['lives'] - 1}---------------")
            EF_PLAYER["lives"] = player["lives"]
        else:
            POS_ENEMY = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
            EF_ENEMY["power"] = player["power"]
            # EF_ENEMY["lives"] = player["lives"]
    BOMB_PLAYER_DELAY = min(EF_PLAYER["dragonEggDelay"], 3)


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
    global BOMB_POS_LOCK_MINMAX

    global COLS
    global ROWS
    COLS = data["map_info"]["size"]["cols"]
    ROWS = data["map_info"]["size"]["rows"]

    BOMBS = data["map_info"]["bombs"]
    # BOMB_DANGER_POS = get_list_pos_bomb_danger(BOMBS)
    SPOILS = data["map_info"]["spoils"]
    paste_player_data(players=data["map_info"]["players"])
    paste_gst_egg(eggs=data["map_info"]["dragonEggGSTArray"])
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
            EVALUATE_MAP_ROAD[spoil["row"]][spoil["col"]] = 50
            SPOILS_POS.append([spoil["row"], spoil["col"]])
        else:
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = 100
            EVALUATE_MAP_ROAD[spoil["row"]][spoil["col"]] = 0
            # SPOILS_POS.append([spoil["row"], spoil["col"]])


def set_bomb():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    for bomb in BOMBS:
        if bomb["playerId"] in PLAYER_ID:
            set_bomb_point(EF_PLAYER["power"], bomb)
        else:
            set_bomb_point(EF_ENEMY["power"], bomb)


def set_bomb_point(power, bomb):
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_ROAD
    global MAP

    MAP[bomb["row"]][bomb["col"]] = 11  # lock map
    EVALUATE_MAP_PLAYER[bomb["row"]][bomb["col"]] = -DANGER_POINT
    EVALUATE_MAP_ROAD[bomb["row"]][bomb["col"]] = -DANGER_POINT
    EVALUATE_MAP_ENEMY[bomb["row"]][bomb["col"]] = 500

    # handle time => time có thể đi qua
    # handle bomb bị tường chặn => done
    match power:
        case 1:
            for i in BombRange.LV1.value:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -DANGER_POINT
                EVALUATE_MAP_ROAD[bomb["row"] + i[0]][bomb["col"] + i[1]] = -DANGER_POINT
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 2:
            bomb_point_with_lv(bomb, BombRange.LV2.value)
        case 3:
            bomb_point_with_lv(bomb, BombRange.LV3.value)
        case 4:
            bomb_point_with_lv(bomb, BombRange.LV4.value)


def bomb_point_with_lv(bomb, bomb_range) -> int:
    value = 0
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                break
            else:
                EVALUATE_MAP_PLAYER[bomb["row"] + j[0]][bomb["col"] + j[1]] = -DANGER_POINT
                EVALUATE_MAP_ROAD[bomb["row"] + j[0]][bomb["col"] + j[1]] = -DANGER_POINT
                EVALUATE_MAP_ENEMY[bomb["row"] + j[0]][bomb["col"] + j[1]] = 500
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
                if euclid_distance([row, col], POS_PLAYER_EGG) <= 2:
                    continue
                for i in BombRange.LV1.value:  # ko phải bomb nổ :  khoảng cách  =1
                    # a.append([EVALUATE_MAP_ROAD[row + i[0]][col + i[1]], i])
                    EVALUATE_MAP_ROAD[row + i[0]][col + i[1]] = 25
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
    list_row = []
    row = [0] * COLS
    for i in range(ROWS):
        list_row.append(deepcopy(row))

    return list_row


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
    for i in AroundRange.LV1.value:
        EVALUATE_MAP_ROAD[POS_ENEMY_EGG[0] + i[0]][POS_ENEMY_EGG[1] + i[1]] = 25


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
    pass


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


TIME_POINT = 0
ACTION_PER_POINT = 2
RANGE_TIME = 500
COUNT = 0
COUNT_UPDATE = 0
COUNT_ST = 0
TAG_PLAYER = ["player:stop-moving", "player:moving-banned", "bomb:setup"]
HAS_BOMB_ACTION = False

DIRECTION_HIST = []


def ticktack_handler(data):
    global BOMB_POS_LOCK_MINMAX, COUNT, COUNT_UPDATE, COUNT_ST, ACTION_PER_POINT
    global TIME_POINT
    print(data["id"], "-", data.get("player_id", "no id"), "-", data["tag"], "-", data["timestamp"], "-", TIME_POINT)

    print("pos now", data["map_info"]["players"][0]["id"], data["map_info"]["players"][0]["currentPosition"],
          data["map_info"]["players"][1]["currentPosition"])
    paste_player_data(data["map_info"]["players"])

    if data["tag"] in TAG_PLAYER and data["player_id"] in PLAYER_ID:
        TIME_POINT = data["timestamp"]
        COUNT += 1
        print("line 350: ", COUNT, " in ", ACTION_PER_POINT)

    if COUNT == ACTION_PER_POINT:
        pr_yellow("trigger case 1")
    elif data["timestamp"] - TIME_POINT > RANGE_TIME:
        pr_yellow("trigger case 2")

    if COUNT == ACTION_PER_POINT or data["timestamp"] - TIME_POINT > RANGE_TIME:
        ACTION_PER_POINT = 2
        TIME_POINT = data["timestamp"]
        BOMB_POS_LOCK_MINMAX = get_list_pos_bomb_danger(data["map_info"]["bombs"])  # update liên tục
        paste_update_map(data)

        action_case = get_case_action()

        action = get_action(case=action_case)
        print("line 360 case", action_case, action)
        if action_case == 2 and action == []:
            print("find egg")
            action = get_action(case=5)
        print("action:", action)
        if action_case == 1:
            if TMP_POSITION_OBJ is not None:
                act_list, act_list_v2 = action_simulator(TMP_POSITION_OBJ, action)
                direction = dedup_action(act_list, act_list_v2)
            else:
                ACTION_PER_POINT = len(action)
                direction = gen_direction(action)
        elif action_case == 2 and len(action) <= 4:
            ACTION_PER_POINT = len(action)
            direction = gen_direction(action)
        else:
            action = action[0:ACTION_PER_POINT + 1]
            ACTION_PER_POINT = ACTION_PER_POINT + 1
            direction = gen_direction(action)
        pr_green("line 390 direction:" + direction)
        emit_direction(direction)
        ACTION_PER_POINT = max(ACTION_PER_POINT, 2)
        COUNT = 0
        # COUNT_UPDATE = 0


# todo: có vẻ action bị dính nên emit vào bị lêch

def dedup_action(action, action_v2):
    global ACTION_PER_POINT
    direction = gen_direction(action)
    DIRECTION_HIST.append(direction)
    print(DIRECTION_HIST)
    if len(DIRECTION_HIST) >= 6:
        if DIRECTION_HIST.count(direction) >= 3:
            ACTION_PER_POINT = len(action_v2)
            direction = gen_direction(action_v2)
            DIRECTION_HIST.pop()
            DIRECTION_HIST.append(direction)
        DIRECTION_HIST.pop(0)
    if len(direction) != ACTION_PER_POINT:  # re verify
        ACTION_PER_POINT = len(direction)
    # pr_red("line 400 new direction:" + direction)
    return direction


def get_case_action() -> int:
    val_pos = EVALUATE_MAP_ROAD[POS_PLAYER[0]][POS_PLAYER[1]]
    print("pos", POS_PLAYER, "point :", val_pos)
    if bfs_f(POS_PLAYER, [ROWS, COLS]):
        # print("case 1")
        return 1
    if euclid_distance(POS_ENEMY, POS_PLAYER) <= 4:
        # print("case 2")
        return 1
    if val_pos != 0:
        # print("case 3")
        return 1
    elif val_pos == 0:
        # print("case 4")
        return 2


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
        if bomb["playerId"] in PLAYER_ID:
            if bomb["remainTime"] > (400 * BOMB_PLAYER_DELAY):
                p = False
        else:
            e = False
    return p, e


def get_action(case) -> list:
    """
    1 -> action no e \n
    2 -> find pos bomb \n
    3 -> action ab \n
    5 -> find egg enemy \n
    6 -> find egg player \n
    7 -> find enemy ~ kill mode \n
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
                p_zone=is_zone(pos=POS_PLAYER, size=size)
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
        case 7:
            return a_star(
                start=POS_PLAYER,
                target=POS_ENEMY
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


# a star

def a_star(start, target):
    # print(start, target)
    queue = [[start, euclid_distance(start, target), [start], []]]  # pos , dis, pos_list, act_list
    lock_list = [start]  # lọc lặp

    while queue:
        cr_status = queue.pop(0)
        # print(cr_status)
        if cr_status[1] == 1:
            return cr_status[3]
        for act in NextMoveZone.Z4.value:
            new_pos_player = [sum(i) for i in zip(cr_status[0], act)]
            if new_pos_player in BOMB_POS_LOCK_MINMAX:
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
def bfs(start: list, size_map: list, p_zone: int):
    pos_list = [start]  # lọc lặp
    actions = get_move_out_zone(p_zone)
    queue = []
    act_list = []
    try:
        begin_status = [start, []]  # current pos , action to pos

        point, pos_list, end_status = next_pos_bfs(actions, begin_status, pos_list, size_map, queue)
        print("685", point, pos_list, end_status)
        if point >= 25:
            # print("return", end_status[1])
            act_list = end_status[1]
    finally:
        return act_list


def next_pos_bfs(actions, cr_status, pos_list, size_map, queue: list):
    for act in actions:
        new_pos_player = [sum(i) for i in zip(cr_status[0], act)]
        # print("line 630", cr_status, "->", new_pos_player)
        if new_pos_player in pos_list:
            continue
        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST_BFS:
            # print("line 645", new_pos_player, MAP[new_pos_player[0]][new_pos_player[1]])
            continue
        if new_pos_player in BOMB_POS_LOCK_MINMAX:
            continue
        if new_pos_player == POS_ENEMY:
            continue
        point = EVALUATE_MAP_ROAD[new_pos_player[0]][new_pos_player[1]]
        # print("line 650", cr_status, "->", new_pos_player, point, pos_list)
        if point >= 25 and new_pos_player not in BOMB_POS_LOCK_MINMAX:  # not is_danger_bombs(new_pos_player, BOMBS):
            end_status = deepcopy(cr_status)
            end_status[1].append(act)
            end_status[0] = new_pos_player
            pos_list.append(new_pos_player)
            # print("line 655", point, pos_list, end_status)
            return point, pos_list, end_status
        # print("710")
        new_status = deepcopy(cr_status)
        new_status[1].append(act)
        new_status[0] = new_pos_player

        pos_list.append(new_pos_player)
        queue.append(new_status)

    # print("line 730", queue)

    next_status = queue.pop(0)

    point, pos_list, end_status = next_pos_bfs(actions, next_status, pos_list, size_map, queue)

    return point, pos_list, end_status


LEVEL_F = 1


def bfs_f(start: list, size_map: list):
    pos_list = [start]  # lọc lặp
    z = is_zone(start, size_map)
    actions = get_move_in_zone(z)
    queue = []
    result = False
    try:
        begin_status = [start, 0]  # current pos , action to pos

        point, _, _ = next_pos_bfs_f(actions, begin_status, pos_list, size_map, queue)

        if point != 0:
            result = True
    finally:
        # print(result)
        return result


def next_pos_bfs_f(actions, cr_status, pos_list, size_map, queue: list):
    for act in actions:
        new_pos_player = [sum(i) for i in zip(cr_status[0], act)]
        # print("line 715", cr_status, "->", new_pos_player)
        if new_pos_player in pos_list:
            continue
        if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST_BFS:
            # print("line 720", new_pos_player, MAP[new_pos_player[0]][new_pos_player[1]])
            continue

        point = EVALUATE_MAP_ROAD[new_pos_player[0]][new_pos_player[1]]
        if point == 0 and cr_status[1] == LEVEL_F:
            continue
        if point != 0:
            end_status = deepcopy(cr_status)
            end_status[1] = cr_status[1] + 1
            end_status[0] = new_pos_player
            pos_list.append(new_pos_player)
            # print("line 655", point, pos_list, end_status)
            return point, pos_list, end_status

        # print("710")
        new_status = deepcopy(cr_status)
        new_status[1] = cr_status[1] + 1
        new_status[0] = new_pos_player

        pos_list.append(new_pos_player)
        queue.append(new_status)

    # print("line 730", queue)

    next_status = queue.pop(0)

    point, pos_list, end_status = next_pos_bfs_f(actions, next_status, pos_list, size_map, queue)

    return point, pos_list, end_status


# minimax
# init


MAX = 10000000
MIN = -10000000
TELE_POINT = 5000
DANGER_POINT = 10000
P1 = 1  # player
P2 = 2  # enemy


def bomb_bonus(bomb) -> int:
    if bomb["playerId"] in PLAYER_ID:
        return destroy_point(EF_PLAYER["power"], bomb)
    else:
        return destroy_point(EF_ENEMY["power"], bomb)


def destroy_point(power, bomb) -> int:
    point = 0
    match power:
        case 1:
            for i in BombRange.LV1.value:
                if MAP[bomb["row"] + i[0]][bomb["col"] + i[1]] == 2:
                    point += 500
        case 2:
            point += destroy_point_with_lv(bomb, BombRange.LV2.value)
        case 3:
            point += destroy_point_with_lv(bomb, BombRange.LV3.value)
        case _:
            point += destroy_point_with_lv(bomb, BombRange.LV4.value)
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
                break
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 2:
                value += check_bulk_around_egg([bomb["row"] + j[0], bomb["col"] + j[1]])
                break
            if [bomb["row"] + j[0], bomb["col"] + j[1]] == POS_ENEMY_EGG:
                value += 1000
                break
            if [bomb["row"] + j[0], bomb["col"] + j[1]] == POS_PLAYER_EGG:
                value -= 500
                break
    return value


def check_bulk_around_egg(pos):
    if euclid_distance(pos, POS_ENEMY_EGG) <= 2:
        return 700
    elif euclid_distance(pos, POS_PLAYER_EGG) <= 2:
        return 0
    else:
        return 500


def list_pos_bomb(power, bomb) -> list:
    list_pos = [[bomb["row"], bomb["col"]]]
    # print("835 : add list bomb pos")
    match power:
        case 1:
            for i in BombRange.LV1.value:
                # print([bomb["row"] + i[0], bomb["col"] + i[1]], position)
                list_pos.append([bomb["row"] + i[0], bomb["col"] + i[1]])
        case 2:
            list_pos += list_pos_bomb_with_lv(bomb, BombRange.LV2.value)
        case 3:
            list_pos += list_pos_bomb_with_lv(bomb, BombRange.LV3.value)
        case _:
            list_pos += list_pos_bomb_with_lv(bomb, BombRange.LV4.value)
    return list_pos


LIST_NO_DES = [1, 5]


def list_pos_bomb_with_lv(bomb, bomb_range) -> list:
    list_pos = []
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 3:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] in LIST_NO_DES:
                break
            list_pos.append([bomb["row"] + j[0], bomb["col"] + j[1]])
    return list_pos


REMAIN_TIME_LOCK = 600
TIME_UNLOCK = 700


def get_list_pos_bomb_danger(bombs):
    list_pos = []
    print("line 805:", bombs)
    for bomb in bombs:
        if bomb["remainTime"] > 900:
            continue
        if bomb["remainTime"] < REMAIN_TIME_LOCK:
            if bomb not in BOMBS_:
                BOMBS_.append(bomb)
                BOMBS_L2.append(TIME_POINT)
        if bomb["playerId"] in PLAYER_ID:
            list_pos += list_pos_bomb(EF_PLAYER["power"], bomb)
        else:
            list_pos += list_pos_bomb(EF_ENEMY["power"], bomb)
    print("line 815: bomb pos s1", list_pos)
    """"""
    while BOMBS_L2:
        if TIME_POINT - BOMBS_L2[0] > TIME_UNLOCK:
            BOMBS_L2.pop(0)
            BOMBS_.pop(0)
        else:
            break
    print("list bomb keep", BOMBS_)
    print("list bomb keep", BOMBS_L2)
    for bomb in BOMBS_:
        if bomb["playerId"] in PLAYER_ID:
            list_pos += list_pos_bomb(EF_PLAYER["power"], bomb)
        else:
            list_pos += list_pos_bomb(EF_ENEMY["power"], bomb)
    print(list_pos)
    return list_pos


def is_danger_bombs(position, bombs) -> bool:
    """

    :param position:
    :param bombs: [{col,row,playerId}]
    :return:
    """
    # print("check danger", position, bombs)
    for bomb in bombs:
        if bomb["playerId"] in PLAYER_ID:
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
    if bomb["playerId"] in PLAYER_ID:
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
        case 3:
            return is_pos_danger_with_lv(bomb, BombRange.LV3.value, position)
        case _:
            return is_pos_danger_with_lv(bomb, BombRange.LV4.value, position)
    return False


def is_pos_danger_with_lv(bomb, bomb_range, position) -> int:
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                break
            if [bomb["row"] + j[0], bomb["col"] + j[1]] == position:
                return True
    return False


def val(position: Position, list_pos=None, list_act=None) -> int:
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
    # print("check val", list_pos)
    global COUNT
    COUNT = COUNT + 1
    # print("count", COUNT, position)
    if position.bombs:
        for bomb in position.bombs:
            if is_danger_bomb(position.pos_player, bomb):
                value -= DANGER_POINT
            if is_danger_bomb(position.pos_enemy, bomb):
                value += 1000
            if bomb["playerId"] in PLAYER_ID:
                value += bomb_bonus(bomb) * 1.5

            if list_pos is not None and bomb.get("old", False):
                # if list_pos == [[3, 4], [2, 4], [2, 4], [1, 4], [1, 5]]:
                #    print(value)
                for idx, x in enumerate(list_pos, start=1):
                    if is_danger_bomb(x, bomb):
                        value += match_idx_bomb(idx)
                #   print(idx, value)
                # if list_pos == [[3, 4], [2, 4], [2, 4], [1, 4], [1, 5]]:
                #    print(value)


    # tính theo pos nên bị lệch vs điểm start đặt bomb => case trên -800
    else:
        pass

    if list_pos is not None:
        """
        if list_pos == [[2, 11], [1, 11], [1, 12], [2, 12], [3, 12], [3, 11]]:
            print("line 935", SPOILS_POS)
            va = value

            for idx, x in enumerate(list_pos[0:4], start=1):
                print(idx, x, x in SPOILS_POS, match_idx_spoil(idx))
                if x in SPOILS_POS:
                    va += match_idx_spoil(idx)
                    va += 200
            print(va)
        """
        # if list_pos == [[3, 4], [2, 4], [2, 4], [1, 4], [1, 5]]:
        #    print(value)
        for idx, x in enumerate(list_pos[0:4], start=1):
            if x in SPOILS_POS:
                value += match_idx_spoil(idx)
                value += 200
        # if list_pos == [[3, 4], [2, 4], [2, 4], [1, 4], [1, 5]]:
        #    print(value)
    return value


def match_idx_spoil(idx):
    match idx:
        case 1:
            return 400
        case 2:
            return 200
        case 3:
            return 100
        case _:
            return 50


# để đăt đc bom case 1 đường thifif min  > sum 3 step
def match_idx_bomb(idx):
    match idx:
        case 1:
            return -100
        case 2:
            return -200
        case 3:
            return -400
        case 4:
            return -1600
        case _:
            return -3200


def check_pos_can_go(new_pos, position: Position):
    list_pos = [position.pos_enemy]
    for bomb in position.bombs:
        list_pos.append([bomb["row"], bomb["col"]])
    if new_pos in list_pos:
        return False
    return True


TMP_POSITION_OBJ: Position


def action_simulator(position: Position, act_list):
    position_clone = deepcopy(position)
    new_acts = []
    new_acts_v2 = new_acts
    check_point_v2 = False
    print("line 1000", ACTION_PER_POINT)
    for idx, act in enumerate(act_list, start=1):
        match act:
            case [1, 1]:
                if check_point_v2:
                    new_acts_v2.append(act)
                    break
                else:
                    position_clone.bombs.append(
                        {
                            "row": position_clone.pos_player[0],
                            "col": position_clone.pos_player[1],
                            "playerId": PLAYER_ID
                        }
                    )
                    new_acts.append(act)
            case [0, 0]:
                break
            case _:
                if check_point_v2:
                    new_acts_v2.append(act)
                    break
                else:
                    new_pos_player = [sum(i) for i in zip(position.pos_player, act)]
                    position_clone.pos_player = new_pos_player
                    new_acts.append(act)
                    if val(position=position_clone) >= -TELE_POINT and idx >= ACTION_PER_POINT + 1:
                        new_acts_v2 = deepcopy(new_acts)
                        check_point_v2 = True
                        pr_yellow(f"{position_clone} point: {val(position=position_clone)}")
    print("line 1030", new_acts, new_acts_v2)
    return new_acts, new_acts_v2


H_NOE = 4  # dộ sâu

DIF_H_NO_BOMB = 2


def minimax_no_e(position: Position, zone: int) -> list:
    value = MIN
    # print(position)
    pos_list = [position.pos_player]
    act_list = []
    global TMP_POSITION_OBJ
    TMP_POSITION_OBJ = deepcopy(position)

    try:
        actions = get_action_out_zone(zone)
        # print("list action: ", actions)

        for act in actions:
            match act:
                case [1, 1]:
                    # print(f"{act_list} action:{act} level:0 ")
                    if not position.bomb_player:
                        continue
                    new_position = deepcopy(position)
                    new_position.bomb_player = False

                    new_position.bombs = deepcopy(position.bombs)
                    new_position.bombs.append(
                        {
                            "row": new_position.pos_player[0],
                            "col": new_position.pos_player[1],
                            "playerId": PLAYER_ID,
                            "old": True
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
                    # print(f"1100 action:{act} level:{0}")
                    if new_pos_player in BOMB_POS_LOCK_MINMAX:
                        continue
                    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST_MAX:
                        continue
                    if not check_pos_can_go(new_pos_player, position):
                        continue
                    if new_pos_player == POS_ENEMY:
                        continue
                    if MAP[new_pos_player[0]][new_pos_player[1]] == 3:
                        new_position = deepcopy(position)
                        new_position.pos_player = new_pos_player
                        # bên trên đã thay đổi nên dưới dugn lại bị sai
                        new_pos_list = deepcopy([position.pos_player])
                        new_act_list = deepcopy([])
                        new_act_list.append(act)
                        point_no_e, pos, move = -TELE_POINT, new_pos_list, new_act_list
                    else:
                        new_position = deepcopy(position)
                        new_position.pos_player = new_pos_player
                        # bên trên đã thay đổi nên dưới dugn lại bị sai
                        new_pos_list = deepcopy([position.pos_player, new_pos_player])
                        new_act_list = deepcopy([])
                        new_act_list.append(act)
                        point_no_e, pos, move = max_val_no_e(new_position, actions, 1, new_pos_list, new_act_list)
                    if value <= point_no_e:
                        # print(f"1190 action:{act} level:{0} point: {point_no_e}  {move} yes")
                        value = point_no_e
                        act_list = move
                        pos_list = pos

    finally:
        pass

    pr_green(f"minimax out: value:{value}  pos_list: {pos_list}act_list:{act_list}")
    return act_list


def max_val_no_e(position: Position, actions, level, pos_list: list, act_list):
    value = MIN
    move = []
    pos = []
    try:
        for act in actions:
            match act:
                case [1, 1]:
                    if level <= DIF_H_NO_BOMB:
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
                    # print(f"1150 {act_list} action:{act}, val: {value} level:{level} ")
                    point_max_no_e = val(position, pos_list)
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
                    # print(f"1165 {act_list} action:{act} level:{level} ")
                    point_max_no_e, pos_l, move_l = move_action(position=position, current_action=act, actions=actions,
                                                                level=level,
                                                                pos_list=pos_list, move_list=act_list)
                    # print("1170 ", point_max_no_e, pos_l, move_l)
                    if value <= point_max_no_e:
                        # print(f"1235 action:{act} level:{level} point: {point_max_no_e} {pos_l} {move_l}")
                        value = point_max_no_e
                        move = move_l
                        pos = pos_l
                    # print("1175 - end act", move, "point:", value, "level", level)
        # print("1176 - end lev", move, "point:", value, "level", level)
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
            "playerId": PLAYER_ID,
            "old": True
        }
    )

    new_pos_list = deepcopy(list_pos)
    new_move_list = deepcopy(list_move)
    new_move_list.append([1, 1])
    new_pos_list.append(deepcopy(position.pos_player))

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
    # print("1210 ", new_pos_player)
    if new_pos_player in BOMB_POS_LOCK_MINMAX:  # and BOMB_PLAYER_ENABLE
        # print("move lock case 1")
        return MIN, pos_list, move_list
    """
    if level >= 2 and new_pos_player in BOMB_DANGER_POS:
        return MIN, pos_list, move_list
    """
    if not check_pos_can_go(new_pos_player, position):
        # print("move lock case 2")
        return MIN, pos_list, move_list
    if MAP[new_pos_player[0]][new_pos_player[1]] in NO_LIST_MAX:
        # print("move lock case 3", MAP[new_pos_player[0]][new_pos_player[1]])
        return MIN, pos_list, move_list
    if MAP[new_pos_player[0]][new_pos_player[1]] == 3:
        # print("1220", move_list, "moved", current_action)
        return -TELE_POINT, pos_list, move_list
    if new_pos_player in pos_list:  # list check đã đi qua
        # print("move lock case 4")
        return MIN, pos_list, move_list
    if new_pos_player == POS_ENEMY:
        # print("move lock case 5")
        return MIN, pos_list, move_list
    # print("1225", move_list, "moving", current_action)
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
        # print("1240 - move end", new_move_list, "point:", val(position=new_position, list_pos=new_pos_list), "level",              level)
        return val(position=new_position, list_pos=new_pos_list), new_pos_list, new_move_list


if __name__ == '__main__':
    connect_server()
    join_game(
        game_id=GAME_ID,
        player_id=PLAYER_ID
    )
