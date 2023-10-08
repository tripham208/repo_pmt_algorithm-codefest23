from gst import PLAYER_ID
from gst.model.const import BombRange

MAP_DEFAULT = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 1],
               [1, 2, 5, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 3, 0, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 0, 3, 0, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 5, 2, 1],
               [1, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 1, 4, 4, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

MAP = []
EVALUATE_MAP_PLAYER = []
EVALUATE_MAP_ENEMY = []
EVALUATE_MAP_ROAD = []
COLS = 0
ROWS = 0

POS_PLAYER = [11, 3]  # row - col
POS_ENEMY = [5, 15]

POS_PLAYER_EGG = [5, 10]  # row - col
POS_ENEMY_EGG = [5, 15]

BOMBS = []
SPOILS = []
EF_PLAYER = {
    "power": 1,
    "lives": 3
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


def mock_default():
    for i in MAP_DEFAULT:
        MAP.append(i.copy())
        EVALUATE_MAP_PLAYER.append(i.copy())
        EVALUATE_MAP_ENEMY.append(i.copy())
        EVALUATE_MAP_ROAD.append(i.copy())
    replace_point_map()


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
    print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)
    reset_point_map()
    replace_point_map(MAP)


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

    global COLS
    global ROWS
    COLS = data["map_info"]["size"]["cols"]
    ROWS = data["map_info"]["size"]["rows"]

    BOMBS = data["map_info"]["bombs"]
    SPOILS = data["map_info"]["spoils"]
    paste_player_data(players=data["map_info"]["players"])

    print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)
    tee()
    MAP = data["map_info"]["map"]
    reset_point_map()
    replace_point_map(),


def tee():
    print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)


def set_spoil():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_ROAD
    for spoil in SPOILS:
        if spoil["spoil_type"] in [3, 4, 5]:  # type egg can use
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = 200
            EVALUATE_MAP_ENEMY[spoil["row"]][spoil["col"]] = -200
            EVALUATE_MAP_ROAD[spoil["row"]][spoil["col"]] += 50
        else:
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = -200
            # MAP[spoil["row"]][spoil["col"]] = 16  # lock map


def show_map_info():
    print(f"size: {COLS} - {ROWS}")


def point(player, obj) -> int:
    """
    set point theo player/obj ngoại trừ trứng
    :param player:
    1: player
    2: enemy
    :param obj:
    :return:
    """
    match [player, obj]:
        case _:
            return 0


'''    
        move map point => bonus point

        case [1, 2]:
            return 200
        case [2, 2]:
            return -200
                case [1, 3]:
            return 300
   
'''


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
    # handle bomb bị tường chặn => done but not verify
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
                EVALUATE_MAP_ROAD[bomb["row"] + j[0]][bomb["col"] + j[1]] = 500
    return value


def replace_point_map(first=False):
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global BOMBS
    if first:
        for row in range(ROWS):
            for col in range(COLS):
                if MAP[row][col] == 2:
                    for i in BombRange.LV1.value:
                        EVALUATE_MAP_ROAD[row + i[0]][col + i[1]] += 25
                    '''
                    EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                    EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])'''
        set_addition_point()
    else:
        for row in range(ROWS):
            for col in range(COLS):
                if MAP[row][col] == 2:
                    for i in BombRange.LV1.value:
                        EVALUATE_MAP_ROAD[row + i[0]][col + i[1]] += 25

                '''
                # only map change update point todo: check this
                # map change khi có gỗ bị phá vậy thì có cần up date point ko?
                if MAP[row][col] == current_map[row][col]:
                    pass
                else:
                    EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                    EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])'''
        set_addition_point()


def reset_point_map():
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ROAD
    EVALUATE_MAP_PLAYER = [[0] * COLS] * ROWS
    EVALUATE_MAP_ENEMY = [[0] * COLS] * ROWS
    EVALUATE_MAP_ROAD = [[0] * COLS] * ROWS


def set_addition_point():
    set_bomb()
    set_spoil()


# todo: val function handle bomb + point replace point from map but how to point + khi nổ thùng vs đứng trong bom

"""
    NOTE
- cmt code map -> point map

"""
