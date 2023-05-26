import datetime

from ..utils.tasks import validate_arguments
from ...components import Module
from ...components import Task
from ...exceptions.managers.tasks import CreateTaskError
from ...managers import ModulesManager
from ...managers import TasksManager

MODULES_MANAGER = ModulesManager()
TASKS_MANAGER = TasksManager()


async def create_task(module: str | Module, launch_time: datetime.datetime = None, **kwargs):
    if not isinstance(module, str) and not isinstance(module, Module):
        raise CreateTaskError("Argument 'module' must be an Module or module name.")

    module = module if isinstance(module, Module) else MODULES_MANAGER.modules.get(module)
    if not module:
        raise CreateTaskError(f"There is no module named {module}")

    validate_arguments(func_args=module.task_FC.args, task_args=kwargs)

    task = Task(launch_time=launch_time, **kwargs)
    await TASKS_MANAGER.add_task(module=module, task=task)
