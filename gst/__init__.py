import socketio

from main import ENEMY_ID
from gst.map_handler import *

URL = 'http://localhost:1563/'

JOIN_GAME_EVENT = 'join game'
TICKTACK_EVENT = "ticktack player"
DRIVE_EVENT = "drive player"

sio = socketio.Client()


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


# print(f"ticktack:{data}")


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
