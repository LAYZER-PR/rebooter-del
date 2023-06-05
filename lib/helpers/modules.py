from ...components.function import FunctionContainer as FC
from ...components.module import Module
from ...managers import ModulesManager

MANAGER = ModulesManager()


async def create_module(
        name: str,
        task_function: FC,
        exc_function: FC = None,
        threads: int = 1,
        rotation: int = 10
) -> Module:
    module = Module(
        name=name,
        task_function=task_function,
        exc_function=exc_function,
        threads=threads,
        rotation=rotation
    )
    await MANAGER.add_module(module)
    return module
