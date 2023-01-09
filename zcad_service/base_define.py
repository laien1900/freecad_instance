from enum import Enum


class command_type(Enum):
    NONE_TYPE = -1
    ERROR_MESSAGE = 0
    REGISTER_SERVICE = 1
    NEW_INSTANCE = 2
    CLOSE_INSTANCE = 3
    DELAY_TIME = 4,


def message_process(id):
    return command_type(id)