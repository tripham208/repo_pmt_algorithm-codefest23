def ticktack_handler():
    pass


def gen_direction(direction):
    """
    1 - Move LEFT \n
    2 - Move RIGHT.\n
    3 - Move UP\n
    4 - Move DOWN\n
    b - Drop BOMB\n
    x - Stop Moving\n
    :param direction:
    :return:
    """
    output = ""
    for i in direction:
        match i:
            case [0, -1]:
                output += '1'
            case [0, 1]:
                output += '2'
            case [-1, 0]:
                output += '3'
            case [1, 0]:
                output += '4'
            case [0, 0]:
                output += 'x'
            case [1, 1]:
                output += 'b'
    return output
