import asyncio
import uuid
from itertools import zip_longest

from ..components.function import FunctionContainer as FC
from ..containers.thread import ThreadData
from ..exceptions.components.module import CreateModuleError
from ..lib.constants.statuses import ModuleStatus, TaskStatus, ThreadStatus
from ..lib.helpers.functions import task_func_initiator


class Module:
    __MODULES_MANAGER__ = None  # ModulesManager
    __TASKS_MANAGER__ = None  # TasksManager

    __concurrences__: dict[uuid.UUID, ThreadData] = dict()
    __status__: ModuleStatus = ModuleStatus.ACTIVE

    __thread__: int = 0

    def __init__(
            self,
            name: str,
            task_function: FC,
            exc_function: FC = None,
            rotation: int = 10,
            threads: int = 1,
    ):
        if not name or not isinstance(name, str):
            raise CreateModuleError('name - is not a string')

        if not task_function or not isinstance(task_function, FC):
            raise CreateModuleError('task_function - is not a FunctionContainer')

        if exc_function and not isinstance(exc_function, FC):
            raise CreateModuleError('exc_function - is not a FunctionContainer')

        if not rotation or not isinstance(rotation, int):
            raise CreateModuleError('rotation - is not a digit')

        if not threads or not isinstance(threads, int):
            raise CreateModuleError('threads - is not a digit')

        if exc_function and task_function.args != exc_function.args:
            raise CreateModuleError('The exc_function args must be the same as in task_function args')

        self.__name__: str = name

        self.__task_FC__: FC = task_function
        self.__exc_FC__: FC = exc_function
        self.__rotation__: int = rotation

        self.threads = threads

        asyncio.ensure_future(self.__THREAD_MANAGER__())

    # - - - name - - - #
    @property
    def name(self) -> str:
        return self.__name__

    # - - - task_FC - - - #
    @property
    def task_FC(self) -> FC:

        return self.__task_FC__

    # - - - exc_FC - - - #
    @property
    def exc_FC(self) -> FC:
        return self.__exc_FC__

    # - - - threads - - - #
    @property
    def threads(self) -> int:
        return self.__threads__

    @threads.setter
    def threads(self, threads: int) -> None:
        if not threads or not isinstance(threads, int):
            raise CreateModuleError('threads - is not a digit')

        for thread_num, thread in zip_longest(range(1, threads + 1), self.__concurrences__, fillvalue=None):
            if not thread:
                self.__create_thread__()

            if not thread_num:
                for thread_id, thread_data in self.__concurrences__.items():
                    if thread_data['status'] == ThreadStatus.WAITING:
                        self.__concurrences__[thread_id]['status'] = ThreadStatus.DEACTIVATION
                        break

                for thread_id, thread_data in self.__concurrences__.items():
                    if thread_data['status'] == ThreadStatus.WORKING:
                        self.__concurrences__[thread_id]['status'] = ThreadStatus.DEACTIVATION
                        break

    # - - - rotation - - - #
    @property
    def rotation(self) -> int:
        return self.__rotation__

    @rotation.setter
    def rotation(self, rotation: int) -> None:
        if not rotation or not isinstance(rotation, int):
            raise CreateModuleError('rotation - is not a digit')

        self.__rotation__ = rotation

    # - - - __MODULES_MANAGER__ - - - #

    @property
    def MODULES_MANAGER(self):
        if self.__MODULES_MANAGER__ is None:
            from .. import ModulesManager
            self.__MODULES_MANAGER__ = ModulesManager()
        return self.__MODULES_MANAGER__

    @MODULES_MANAGER.setter
    def MODULES_MANAGER(self, value):
        self.__MODULES_MANAGER__ = value

    # - - - __TASKS_MANAGER__ - - - #

    @property
    def TASKS_MANAGER(self):
        if self.__TASKS_MANAGER__ is None:
            from .. import TasksManager
            self.__TASKS_MANAGER__ = TasksManager()
        return self.__TASKS_MANAGER__

    @TASKS_MANAGER.setter
    def TASKS_MANAGER(self, value):
        self.__TASKS_MANAGER__ = value

    # - - - METHODS - - - #

    def __create_thread__(self) -> None:
        thread_id = uuid.uuid4()
        asyncio.ensure_future(self.__THREAD_SLOT__(thread_id=thread_id))
        self.__concurrences__.setdefault(thread_id, ThreadData(status=ThreadStatus.WAITING, task=None))

    async def __THREAD_SLOT__(self, thread_id: uuid.UUID) -> None:
        while True:
            await asyncio.sleep(self.rotation)

            if self.__status__ is not ModuleStatus.ACTIVE:
                continue

            thread_data = self.__concurrences__[thread_id]
            match thread_data['status']:
                case ThreadStatus.DEACTIVATION:
                    del self.__concurrences__[thread_id]
                    return
                case ThreadStatus.WAITING:
                    continue

            task_id, task = list(thread_data['task'].items())[0]
            result = await task_func_initiator(
                task_fc=self.task_FC,
                exc_fc=self.exc_FC,
                args=task.arguments
            )

            task.status = TaskStatus.COMPLETED
            task.result = result

            self.__concurrences__[thread_id]['status'] = ThreadStatus.WAITING
            self.__concurrences__[thread_id]['task'] = None

    async def __THREAD_MANAGER__(self) -> None:
        while True:
            # print(self.__concurrences__)
            await asyncio.sleep(self.rotation)

            if self.__status__ is not ModuleStatus.ACTIVE:
                continue

            gen = self.TASKS_MANAGER.get_tasks(module=self.name, status=TaskStatus.WAITING, now_time=True)
            for thread_id, thread in self.__concurrences__.items():
                if thread['status'] is ThreadStatus.WAITING:
                    try:
                        task = await anext(gen)
                        list(task.items())[0][1].status = TaskStatus.WORKING

                        self.__concurrences__[thread_id]['task'] = task
                        self.__concurrences__[thread_id]['status'] = ThreadStatus.WORKING

                    except StopAsyncIteration:
                        break
