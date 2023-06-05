from typing import TypedDict

from ..components.task import Task
from ..lib.constants.statuses import ThreadStatus


class ThreadData(TypedDict):
    status: ThreadStatus
    task: Task
