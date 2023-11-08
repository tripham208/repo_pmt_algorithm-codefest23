from gst.handler import show_map
from gst.model.const import BombRange

LIST_NO_DES = [1, 5]
ROWS = 13
COLS = 13
MAP = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def list_pos_bomb_with_lv(bomb, bomb_range):
    list_pos = []
    for i in bomb_range:
        for j in i:
            if bomb["row"] + j[0] < 0 or bomb["row"] + j[0] >= ROWS:
                continue
            if bomb["col"] + j[1] < 0 or bomb["col"] + j[1] >= COLS:
                continue
            if MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] in LIST_NO_DES:  # todo check lại vụ cản xem đúng chưa
                break
            MAP[bomb["row"] + j[0]][bomb["col"] + j[1]] = 9


if __name__ == '__main__':
    list_pos_bomb_with_lv({
        "row": 6,
        "col": 6,
    },BombRange.LV4.value)
    show_map(MAP)
