from gst import JOIN_GAME_EVENT, TICKTACK_EVENT, paste_base_map, paste_update_map, DRIVE_EVENT, \
    ENEMY_ID, URL
from gst.handler import sio, DELAY_FRAME_TIME


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
    match data["id"]:
        case 1:
            paste_base_map(data)
        case x if x % DELAY_FRAME_TIME == 0:
            paste_update_map(data)


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


# todo: handle theo ticktack
# todo: handle theo drive

"""
    có xử lý tính toán trước bom nổ ra spoil ko?
"""
