from typing import TypedDict

from ..constants.statuses import TaskStatus
from ...components.module import Module
from ...components.task import Task
from ...managers import TasksManager

TASK_MANAGER = TasksManager()


class RESULTS(TypedDict):
    tasks: dict[int, Task]
    results: list[any]


async def get_results(module: str | Module, task: int = None) -> RESULTS:
    tasks = await TASK_MANAGER.get_tasks(module=module, task=task, status=TaskStatus.COMPLETED)
    results = RESULTS(tasks=tasks, results=[task.result for task in tasks])
    return results
