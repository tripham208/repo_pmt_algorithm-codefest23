import math as m

from gst.handler.map_handler import POS_ENEMY, ROWS, COLS, MAP


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
    print(POS_PLAYER)
    zp = is_zone(POS_PLAYER, [ROWS, COLS])
    ze = is_zone(POS_ENEMY, [ROWS, COLS])
    if zp != ze and (euclid_distance(POS_ENEMY, POS_PLAYER) >= 4):
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
