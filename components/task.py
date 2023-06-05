import datetime

from ..exceptions.components.task import *
from ..lib.constants.statuses import TaskStatus


class Task:
    __result__: any
    __status__: TaskStatus = TaskStatus.WAITING

    def __init__(self, launch_time=None, **kwargs):
        match type(launch_time):
            case datetime.datetime:
                self.__launch_time__ = launch_time

            case datetime.timedelta:
                self.__launch_time__ = datetime.datetime.now() + launch_time

            case _:
                self.__launch_time__ = datetime.datetime.now()

        self.__arguments__ = kwargs

    @property
    def status(self) -> TaskStatus:
        return self.__status__

    @status.setter
    def status(self, status: TaskStatus) -> None:
        if not isinstance(status, TaskStatus):
            raise SetTaskStatusError("Argument 'status' must be an TaskStatus.")

        match self.status:
            case TaskStatus.WAITING:
                if status not in [TaskStatus.STOPED, TaskStatus.WORKING, TaskStatus.COMPLETED]:
                    raise SetTaskStatusError(
                        "You cannot set this status. Available: STOPED, WORKING and COMPLETED.")

            case TaskStatus.STOPED:
                if status not in [TaskStatus.WAITING, TaskStatus.WORKING, TaskStatus.COMPLETED]:
                    raise SetTaskStatusError(
                        "You cannot set this status. Available: WAITING, WORKING and COMPLETED.")

            case TaskStatus.WORKING:
                if status is not TaskStatus.COMPLETED:
                    raise SetTaskStatusError(
                        "You cannot set this status. Available: COMPLETED.")

            case TaskStatus.COMPLETED:
                raise SetTaskStatusError("It is forbidden to set the status.")

        self.__status__ = status

    @property
    def launch_time(self) -> datetime.datetime:
        return self.__launch_time__

    @launch_time.setter
    def launch_time(self, launch_time: datetime.datetime = None) -> None:

        match type(launch_time):
            case datetime.datetime:
                if launch_time < datetime.datetime.now():
                    raise SetTaskLaunchTimeError("The time point passed in the argument 'launch_time' has expired.")

                self.__launch_time__ = launch_time

            case datetime.timedelta:
                self.__launch_time__ = datetime.datetime.now() + launch_time

            case _:
                self.__launch_time__ = datetime.datetime.now()

    @property
    def result(self) -> any:
        return self.__result__

    @result.setter
    def result(self, result: any):
        self.__result__ = result

    @property
    def arguments(self) -> dict:
        return self.__arguments__
