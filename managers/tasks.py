import datetime

from simple_singleton import Singleton

from ..components import Module
from ..components import Task
from ..exceptions.managers.tasks import AddTaskError, GetTasksError
from ..lib.constants.statuses import TaskStatus


class TasksManager(metaclass=Singleton):
    __tasks__: dict[str, dict[int, Task]] = dict()

    def __init__(self):
        pass

    async def get_tasks(
            self,
            module: str | Module,
            tasks: int | list[int] = None,
            status: TaskStatus | list[TaskStatus] = None,
            now_time: bool = None
    ) -> dict[int, Task]:

        if not isinstance(module, str) and not isinstance(module, Module):
            raise GetTasksError("Argument 'module' must be an Module or module name.")

        if tasks:
            if isinstance(tasks, int):
                tasks = [tasks]

            elif isinstance(tasks, list):
                if not all(isinstance(s, int) for s in tasks):
                    raise GetTasksError(
                        "All elements of the 'tasks' list must be integer values.")
            else:
                raise GetTasksError(
                    "Argument 'tasks' must be a integer value, a list of integer values, or None.")

        if status:
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

        if tasks:
            for number in tasks:
                task_obj = module_tasks.get(number)
                if task_obj:
                    if now_time and task_obj.launch_time > datetime.datetime.now():
                        continue

                    if status and task_obj.status not in status:
                        continue

                    yield {number: task_obj}


        elif status:
            for number, task_obj in module_tasks.items():
                if task_obj.status in status:
                    if now_time and task_obj.launch_time > datetime.datetime.now():
                        continue

                    yield {number: task_obj}

        else:
            for number, task_obj in module_tasks.items():
                if now_time and task_obj.launch_time > datetime.datetime.now():
                    continue
                yield {number: task_obj}

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
