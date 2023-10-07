from main import PLAYER_ID

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

DELAY_FRAME_TIME = 5
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
    "power": 1
}
EF_ENEMY = {
    "power": 1
}

NO_LIST = [1, 2, 3, 11, 16]
"""
0 - A Road \n
1 - A Wall (None destructible cell)\n
2 - A Balk (Destructible cell)\n
3 - A Teleport Gate\n
4 - A Quarantine Place \n
5 - A Dragon Egg GST\n

11 - BOMB \n
16 - 
"""


# todo
#
#
#


def mock_default():
    for i in MAP_DEFAULT:
        MAP.append(i.copy())
        EVALUATE_MAP_PLAYER.append(i.copy())
        EVALUATE_MAP_ENEMY.append(i.copy())


def map_copy(current_map):
    m = []
    for i in current_map:
        m.append(i.copy())
    return m


def ticktack_handler():
    pass


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
    EVALUATE_MAP_PLAYER = data["map_info"]["map"]
    EVALUATE_MAP_ENEMY = data["map_info"]["map"]
    replace_point_map(MAP)


def paste_player_data(players):
    global POS_PLAYER
    global POS_ENEMY
    global EF_PLAYER
    global EF_ENEMY
    for player in players:
        match player["id"]:
            case "player1-xxx":  # todo common player id
                POS_PLAYER = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
                EF_PLAYER["power"] = player["power"]
            case "player2-xxx":
                POS_ENEMY = [player["currentPosition"]["row"], player["currentPosition"]["col"]]
                EF_ENEMY["power"] = player["power"]


def paste_update_map(data):
    """handler update ticktack"""
    global MAP
    global BOMBS
    global SPOILS
    BOMBS = data["map_info"]["bombs"]
    SPOILS = data["map_info"]["spoils"]
    paste_player_data(players=data["map_info"]["players"])
    replace_point_map(current_map=data["map_info"]["map"]),
    MAP = data["map_info"]["map"]


def set_spoil():  # todo add spoil to map? then set point / NO -> keep map and just set point
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    for spoil in SPOILS:
        if spoil["spoil_type"] in [3, 4, 5]:  # type egg can use
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = 200
            EVALUATE_MAP_ENEMY[spoil["row"]][spoil["col"]] = -200
        # sử dụng khi cho phép ăn trứng mystic
        # todo : + point thêm trên đường?
        """
        else:
            EVALUATE_MAP_PLAYER[spoil["row"]][spoil["col"]] = -500
        """


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
            
        p
   
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

    lv1 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    lv2 = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, -2], [2, 0], [0, 2], [-2, 0]]
    lv3 = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, -2], [2, 0], [0, 2], [-2, 0], [0, -3], [3, 0], [0, 3], [-3, 0]]
    MAP[bomb["row"]][bomb["col"]] = 11
    # todo :handle time
    match power:
        case 1:
            for i in lv1:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 2:
            for i in lv2:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500
        case 3:
            for i in lv3:
                EVALUATE_MAP_PLAYER[bomb["row"] + i[0]][bomb["col"] + i[1]] = -500
                EVALUATE_MAP_ENEMY[bomb["row"] + i[0]][bomb["col"] + i[1]] = 500


def replace_point_map(current_map: list[list], first=False):
    global EVALUATE_MAP_PLAYER
    global EVALUATE_MAP_ENEMY
    global BOMBS
    if first:
        for row in range(ROWS):
            for col in range(COLS):
                EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])
        set_addition_point()
    else:
        for row in range(ROWS):
            for col in range(COLS):
                # only map change update point todo: check this
                # map change khi có gỗ bị phá vậy thì có cần up date point ko?
                if MAP[row][col] == current_map[row][col]:
                    pass
                else:
                    EVALUATE_MAP_PLAYER[row][col] = point(1, current_map[row][col])
                    EVALUATE_MAP_ENEMY[row][col] = point(2, current_map[row][col])
        set_addition_point()


def set_addition_point():
    set_bomb()
    set_spoil()


# todo: val function handle bomb + point replace point from map but how to point + khi nổ thùng vs đứng trong bom

"""
-- code replaced

"""
