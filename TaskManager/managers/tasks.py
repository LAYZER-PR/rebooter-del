from simple_singleton import Singleton

from ..components import Module
from ..components import Task
from ..exceptions.managers.tasks import AddTaskError, GetTasksError
from ..lib.constants.statuses import TaskStatus


class TasksManager(metaclass=Singleton):
    __tasks__: dict[str, dict[int, Task]] = dict()

    def __init__(self):
        pass

    async def get_tasks(self, module: str | Module, task: int = None, status: TaskStatus | list[TaskStatus] = None
                        ) -> dict[int, Task]:

        if not isinstance(module, str) and not isinstance(module, Module):
            raise GetTasksError("Argument 'module' must be an Module or module name.")

        if task is not None and not isinstance(task, int):
            raise GetTasksError("Argument 'task' must be an integer or None.")

        if status is not None:
            if isinstance(status, TaskStatus):
                status = [status]

            elif isinstance(status, list):
                if not all(isinstance(s, TaskStatus) for s in status):
                    raise GetTasksError(
                        "All elements of the 'status' list must be instances of the 'TaskStatus'.")
            else:
                raise GetTasksError(
                    "Argument 'status' must be a TaskStatus value, a list of TaskStatus values, or None.")

        module = module if isinstance(module, str) else module.name

        module_tasks = self.__tasks__.get(module, {})
        result_tasks = {}

        if isinstance(task, int):
            task_obj = module_tasks.get(task)
            if task_obj:
                yield {task: task_obj}
                # result_tasks[task] = task_obj

        if status is not None:
            if isinstance(status, list):
                for number, task_obj in module_tasks.items():
                    if task_obj.status in status:
                        yield {number: task_obj}

            else:
                for number, task_obj in module_tasks.items():
                    if task_obj.status == status:
                        yield {number: task_obj}

                        # result_tasks[number] = task_obj

        if not task and not status:
            yield module_tasks

        # return result_tasks

    async def add_task(self, module: Module, task: Task) -> bool:
        if not isinstance(module, Module):
            raise AddTaskError("Argument 'module' must be an Module.")

        if not isinstance(task, Task):
            raise AddTaskError("Argument 'task' must be an Task.")

        module_tasks = self.__tasks__.get(module.name, {})
        self.__tasks__[module.name] = module_tasks
        self.__tasks__[module.name][len(module_tasks) + 1] = task

        return True
