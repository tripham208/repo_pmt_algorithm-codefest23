import socketio

DELAY_FRAME_TIME = 5

sio = socketio.Client()


def show_map(map):
    for i in map:
        print(i)
    print("")

