from enum import Enum


class TaskStatus(Enum):
    WAITING = "WAITING"
    STOPED = "STOPED"
    WORKING = "WORKING"
    COMPLETED = "COMPLETED"


class ThreadStatus(Enum):
    WAITING = "WAITING"
    WORKING = "WORKING"
    DEACTIVATION = "DEACTIVATION"


class ModuleStatus(Enum):
    ACTIVE = "ACTIVE"
    STOPED = "STOPED"
