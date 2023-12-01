from gst.handler import show_map
from gst.model.const import BombRange
from gst.model.position import Position

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


A = None

def a():
    global A
    A = Position(
        pos_player=[1, 2],
        pos_enemy=[2, 3],
        bomb_player=True,
        bomb_enemy=True
    )

    print(A)

    A = Position(
        pos_player=[1, 2],
        pos_enemy=[2, 6],
        bomb_player=False,
        bomb_enemy=True
    )
    print(A)
if __name__ == '__main__':
    a()
