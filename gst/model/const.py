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
    Z1 = [[0, 0], [1, 1], [0, -1], [-1, 0], [1, 0], [0, 1]]
    Z2 = [[0, 0], [1, 1], [-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[0, 0], [1, 1], [0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[0, 0], [1, 1], [1, 0], [0, 1], [0, -1], [-1, 0]]


class NextActionOutZone(Enum):
    """
    Z1 = [[0, 0], [1, 1], [1, 0], [0, -1], [0, 1], [-1, 0]]
    Z2 = [[0, 0], [1, 1], [1, 0], [-1, 0], [0, -1], [0, 1]]
    Z3 = [[0, 0], [1, 1], [0, 1], [0, -1], [-1, 0], [1, 0]]
    Z4 = [[0, 0], [1, 1], [0, -1], [1, 0], [-1, 0], [0, 1]]
    """
    Z1 = [[1, 1], [1, 0], [0, -1], [0, 1], [-1, 0], [0, 0]]
    Z2 = [[1, 1], [1, 0], [-1, 0], [0, -1], [0, 1], [0, 0]]
    Z3 = [[1, 1], [0, 1], [0, -1], [-1, 0], [1, 0], [0, 0]]
    Z4 = [[1, 1], [0, -1], [1, 0], [-1, 0], [0, 1], [0, 0]]
    """
    Z1 = [[0, 0], [1, 1], [1, 0], [0, 1], [0, -1], [-1, 0]]
    Z2 = [[0, 0], [1, 1], [1, 0], [0, -1], [-1, 0], [0, 1]]
    Z3 = [[0, 0], [1, 1], [0, 1], [-1, 0], [0, -1], [1, 0]]
    Z4 = [[0, 0], [1, 1], [0, -1], [-1, 0], [1, 0], [0, 1]]
    """


class NextActionOutZoneChange(Enum):
    Z1 = [[0, 0], [1, 1], [0, 1], [1, 0], [-1, 0], [0, -1]]
    Z2 = [[0, 0], [1, 1], [0, -1], [1, 0], [0, 1], [-1, 0]]
    Z3 = [[0, 0], [1, 1], [-1, 0], [0, 1], [1, 0], [0, -1]]
    Z4 = [[0, 0], [1, 1], [-1, 0], [0, -1], [0, 1], [1, 0]]


class NextMoveInZone(Enum):
    Z1 = [[0, -1], [-1, 0], [1, 0], [0, 1]]
    Z2 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[1, 0], [0, 1], [0, -1], [-1, 0]]


class NextMoveOutZone(Enum):
    Z1 = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    Z2 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    Z3 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    Z4 = [[-1, 0], [0, -1], [0, 1], [1, 0]]


class NextMoveInHaftZone(Enum):
    Z1 = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    Z2 = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    Z3 = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    Z4 = [[1, 0], [0, 1], [0, -1], [-1, 0]]


class AroundRange(Enum):
    LV1 = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]


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
    LV4 = [
        [[0, -1], [0, -2], [0, -3], [0, -4]],
        [[1, 0], [2, 0], [3, 0], [4, 0]],
        [[0, 1], [0, 2], [0, 3], [0, 4]],
        [[-1, 0], [-2, 0], [-3, 0], [-4, 0]]
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


def get_action_out_zone(region):
    match region:
        case 1:
            return NextActionOutZone.Z1.value
        case 2:
            return NextActionOutZone.Z2.value
        case 3:
            return NextActionOutZone.Z3.value
        case _:
            return NextActionOutZone.Z4.value


def change_action_out_zone(actions):
    match actions:
        case NextActionOutZone.Z1.value:
            return NextActionOutZoneChange.Z1.value
        case NextActionOutZone.Z2.value:
            return NextActionOutZoneChange.Z2.value
        case NextActionOutZone.Z3.value:
            return NextActionOutZoneChange.Z3.value
        case NextActionOutZone.Z4.value:
            return NextActionOutZoneChange.Z4.value
        case NextActionOutZoneChange.Z1.value:
            return NextActionOutZone.Z1.value
        case NextActionOutZoneChange.Z2.value:
            return NextActionOutZone.Z2.value
        case NextActionOutZoneChange.Z3.value:
            return NextActionOutZone.Z4.value
        case NextActionOutZoneChange.Z4.value:
            return NextActionOutZone.Z4.value


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


def get_move_out_zone(region):
    match region:
        case 1:
            return NextMoveOutZone.Z1.value
        case 2:
            return NextMoveOutZone.Z2.value
        case 3:
            return NextMoveOutZone.Z3.value
        case _:
            return NextMoveOutZone.Z4.value


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
