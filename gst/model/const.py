from enum import Enum


class NextMoveZone(Enum):
    Z1 = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    Z2 = [[0, -1], [1, 0], [-1, 0], [0, 1]]
    Z3 = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    Z4 = [[0, -1], [-1, 0], [1, 0], [0, 1]]


class NextActionZone(Enum):
    Z1 = [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    Z2 = [[1, 1], [0, -1], [1, 0], [-1, 0], [0, 1], [0, 0]]
    Z3 = [[1, 1], [0, 1], [-1, 0], [0, -1], [1, 0], [0, 0]]
    Z4 = [[1, 1], [0, -1], [-1, 0], [1, 0], [0, 1], [0, 0]]


class NextActionNoStopZone(Enum):
    Z1 = [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0]]
    Z2 = [[1, 1], [0, -1], [1, 0], [-1, 0], [0, 1]]
    Z3 = [[1, 1], [0, 1], [-1, 0], [0, -1], [1, 0]]
    Z4 = [[1, 1], [0, -1], [-1, 0], [1, 0], [0, 1]]


class NextActionInZone(Enum):
    Z1 = [[1, 1], [0, 0], [0, -1], [-1, 0], [1, 0], [0, 1]]
    Z2 = [[1, 1], [0, 0], [-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[1, 1], [0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[1, 1], [0, 0], [1, 0], [0, 1], [0, -1], [-1, 0]]


class NextMoveInZone(Enum):
    Z1 = [[0, -1], [-1, 0], [1, 0], [0, 1]]
    Z2 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[1, 0], [0, 1], [0, -1], [-1, 0]]


class NextMoveInHaftZone(Enum):
    Z1 = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    Z2 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[1, 0], [0, 1], [0, -1], [-1, 0]]


class BombRange(Enum):
    LV1 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    LV2 = [
        [[0, -1], [0, -2]],
        [[1, 0], [2, 0]],
        [[0, 1], [0, 2]],
        [[-1, 0], [-2, 0]]
    ]
    LV3 = [
        [[0, -1], [0, -2], [0, -3]],
        [[1, 0], [2, 0], [3, 0]],
        [[0, 1], [0, 2], [0, 3]],
        [[-1, 0], [-2, 0], [-3, 0]]
    ]


def get_action_in_zone(region):
    match region:
        case 1:
            return NextActionInZone.Z1.value
        case 2:
            return NextActionInZone.Z2.value
        case 3:
            return NextActionInZone.Z3.value
        case _:
            return NextActionInZone.Z4.value


def get_move_in_zone(region):
    match region:
        case 1:
            return NextMoveInZone.Z1.value
        case 2:
            return NextMoveInZone.Z2.value
        case 3:
            return NextMoveInZone.Z3.value
        case _:
            return NextMoveInZone.Z4.value


def get_action_zone(region):
    match region:
        case 1:
            return NextActionZone.Z1.value
        case 2:
            return NextActionZone.Z2.value
        case 3:
            return NextActionZone.Z3.value
        case _:
            return NextActionZone.Z4.value
