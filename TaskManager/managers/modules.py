from simple_singleton import Singleton

from ..components.module import Module
from ..exceptions.managers.modules import AddModuleError


class ModulesManager(metaclass=Singleton):
    __modules__: dict[str, Module] = {}

    def __init__(self):
        pass

    @property
    def modules(self) -> dict[str, Module]:
        return self.__modules__

    async def add_module(self, module: Module) -> bool:
        if not isinstance(module, Module):
            raise AddModuleError("module - is not a Module")

        if self.__modules__.get(module.name):
            raise AddModuleError("module with this name has already been added")

        self.__modules__[module.name] = module
