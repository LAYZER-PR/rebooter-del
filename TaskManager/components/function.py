import inspect

from ..exceptions.components.function import FunctionError


class FunctionContainer:
    __timeout__ = None
    __retries__ = None
    __retry_delay__ = None

    def __init__(self, func: callable, timeout: int = None, retries: int = None, retry_delay: int = None):
        self.__func__ = func
        self.__async__ = inspect.iscoroutinefunction(func)
        self.__args__ = inspect.signature(func).parameters.items()

        if timeout:
            if isinstance(timeout, int):
                self.__timeout__ = timeout

            elif isinstance(timeout, str) and timeout.isdigit():
                self.__timeout__ = int(timeout)

            else:
                raise FunctionError('The "timeout" must be a number')

        if retries:
            if not timeout:
                raise FunctionError('For retries, you need to specify "timeout"')

            if isinstance(retries, int):
                self.__retries__ = retries

            elif isinstance(retries, str) and retries.isdigit():
                self.__retries__ = int(retries)

            else:
                raise FunctionError('The "retries" must be a number')

        if retry_delay:
            if not retries:
                raise FunctionError('For retry_delay, you need to specify "retries"')

            if isinstance(retry_delay, int):
                self.__retry_delay__ = retry_delay

            elif isinstance(retry_delay, str) and retry_delay.isdigit():
                self.__retry_delay__ = int(retry_delay)

            else:
                raise FunctionError('The "retry_delay" must be a number')

    @property
    def func(self) -> callable:
        return self.__func__

    @property
    def async_type(self) -> bool:
        return self.__async__

    @property
    def args(self) -> dict:
        return self.__args__

    @property
    def timeout(self) -> int | None:
        return self.__timeout__

    @property
    def retries(self) -> int | None:
        return self.__retries__

    @property
    def retry_delay(self) -> int | None:
        return self.__retry_delay__
