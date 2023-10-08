from gst import PLAYER_ID
from gst.handler.map_handler import EF_PLAYER, EF_ENEMY, EVALUATE_MAP_PLAYER, EVALUATE_MAP_ENEMY, MAP, \
    EVALUATE_MAP_ROAD, ROWS, COLS
from gst.model.position import Position
from gst.model.const import BombRange

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

def is_danger(position, bomb) -> bool:
    """

    :param position:
    :param bomb: {col,row,playerId}
    :return:
    """
    # print("check danger", position, bomb)
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
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] == 1:
                continue
            if [bomb["row"] + j[0], bomb["col"] + j[1]] == position:
                return True
    return False


def val(position: Position) -> int:
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

    global COUNT
    COUNT = COUNT + 1
    #print("count", COUNT, position)
    if position.bombs:
        for bomb in position.bombs:
            if is_danger(position.pos_player, bomb):
                value -= 500
            if is_danger(position.pos_enemy, bomb):
                value += 100
            if bomb["playerId"] == PLAYER_ID:
                value += bomb_bonus(bomb) * 1.5
            else:
                value -= bomb_bonus(bomb)
    else:
        pass

    return value


def check_pos_can_go(new_pos, position: Position):
    list_pos = [position.pos_enemy]
    for bomb in position.bombs:
        list_pos.append([bomb["row"], bomb["col"]])
    if new_pos in list_pos:
        return False
    return True


# handle move mul step

# v1
#   5 = 4k3
# a1
#   5 = 900?
# a2
#   5 = 8k7
#   5 ab = 2k3
# no e
#   7 = 41k
#   5 = 2k6
#       5 list pos = 1k9
#       5 no bomb lv1 = 1k4
#       5 no bomb lv1 + list = 1k
#       5 no bomb lv1 + list = 300

