from gst import JOIN_GAME_EVENT, TICKTACK_EVENT, DRIVE_EVENT, ENEMY_ID, URL
from gst.algorithm import is_save_zone, check_half_zone, is_zone, change_haft_zone
from gst.algorithm.fs.bfs import bfs
from gst.handler import sio, DELAY_FRAME_TIME
from gst.handler.action_handler import get_action, gen_direction
from gst.handler.map_handler import paste_base_map, paste_update_map, EVALUATE_MAP_ROAD, POS_PLAYER, ROWS, COLS, \
    POS_ENEMY


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
    print(data["id"])
    match data["id"]:
        case 1:
            paste_base_map(data)
        case x if x % DELAY_FRAME_TIME == 0:
            paste_update_map(data)

            print("col - row", COLS, ROWS, POS_PLAYER, POS_ENEMY)
            action_case = get_case_action()

            action = get_action(case=action_case)

            if action_case == 2 and action == []:
                p_zone = is_zone(pos=POS_PLAYER, size=[ROWS, COLS])
                e_zone = is_zone(pos=POS_ENEMY, size=[ROWS, COLS])
                hz, _ = check_half_zone(p_zone, e_zone)
                new_hz = change_haft_zone(hz, e_zone)
                action = bfs(
                    start=POS_PLAYER,
                    size_map=[ROWS, COLS],
                    p_zone=p_zone,
                    e_zone=e_zone,
                    hz=new_hz
                )
                if not action:
                    pass

            direction = gen_direction(action)

            emit_direction(direction)


def get_case_action() -> int:
    if is_save_zone():
        if EVALUATE_MAP_ROAD[POS_PLAYER[0]][POS_PLAYER[1]] >= 25:
            return 1
        elif EVALUATE_MAP_ROAD[POS_PLAYER[0]][POS_PLAYER[1]] < 25:
            return 2
    else:
        return 3
    return 1


# todo: handle theo ticktack
# todo: handle theo drive

"""
    có xử lý tính toán trước bom nổ ra spoil ko? => nope
"""
