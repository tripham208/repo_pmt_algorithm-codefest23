from gst import PLAYER_ID

MAP_DEFAULT = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 1],
               [1, 2, 5, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 3, 0, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 1],
               [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 1],
               [1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 0, 3, 0, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 5, 2, 1],
               [1, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 1, 4, 4, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

MAP = []
EVALUATE_MAP_PLAYER = []
EVALUATE_MAP_ENEMY = []

COLS = 26
ROWS = 14

POS_PLAYER = [5, 10]  # row - col
POS_ENEMY = [5, 15]

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

NO_LIST = [1, 2, 3, 11, 16]
"""
0 - A Road \n
1 - A Wall (None destructible cell)\n
2 - A Balk (Destructible cell)\n
3 - A Teleport Gate\n
4 - A Quarantine Place \n
5 - A Dragon Egg GST\n

11 - Bomb \n
16 - Mystic egg
"""

LV1 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
LV2 = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, -2], [2, 0], [0, 2], [-2, 0]]
LV3 = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, -2], [2, 0], [0, 2], [-2, 0], [0, -3], [3, 0], [0, 3], [-3, 0]]


#
#
#


def mock_default():
    for i in MAP_DEFAULT:
        MAP.append(i.copy())
        EVALUATE_MAP_PLAYER.append(i.copy())
        EVALUATE_MAP_ENEMY.append(i.copy())


def paste_base_map(data):
    """first handle ticktack"""
    global COLS
    global ROWS
    global MAP
    global EVALUATE_MAP_ENEMY
    global EVALUATE_MAP_PLAYER
    COLS = data["map_info"]["size"]["cols"]
    ROWS = data["map_info"]["size"]["rows"]
    MAP = data["map_info"]["map"]
    paste_player_data(players=data["map_info"]["players"])
    # EVALUATE_MAP_PLAYER = data["map_info"]["map"]
    # EVALUATE_MAP_ENEMY = data["map_info"]["map"]
    reset_point_map()
    replace_point_map(MAP)


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
    """handler update ticktack"""
    global MAP
    global BOMBS
    global SPOILS
    BOMBS = data["map_info"]["bombs"]
    SPOILS = data["map_info"]["spoils"]
    paste_player_data(players=data["map_info"]["players"])
    replace_point_map(current_map=data["map_info"]["map"]),
    reset_point_map()
    MAP = data["map_info"]["map"]


def set_spoil():
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    for spoil in SPOILS:
        if spoil["spoil_type"] in [3, 4, 5]:  # type egg can use
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = 200
            EVALUATE_MAP_ENEMY[spoil["row"]][spoil["col"]] = -200
        # todo : + point thêm trên đường?
        else:
            MAP[spoil["row"]][spoil["col"]] = 16  # lock map


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
    global MAP

    MAP[bomb["row"]][bomb["col"]] = 11  # lock map
    # todo :handle time
    match power:
        case 1:
            for i in LV1:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 2:
            for i in LV2:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 3:
            for i in LV3:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500


def replace_point_map(current_map: list[list], first=False):
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global BOMBS
    if first:
        '''
        for row in range(ROWS):
            for col in range(COLS):
                EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])'''
        set_addition_point()
    else:
        '''
        for row in range(ROWS):
            for col in range(COLS):
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
    EVALUATE_MAP_PLAYER = [[0] * COLS] * ROWS
    EVALUATE_MAP_ENEMY = [[0] * COLS] * ROWS


def set_addition_point():
    set_bomb()
    set_spoil()


# todo: val function handle bomb + point replace point from map but how to point + khi nổ thùng vs đứng trong bom

"""
    NOTE
- cmt code map -> point map

"""
