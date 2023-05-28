from TaskManager.components import FC

from TaskManager.lib.helpers.tasks import create_task
from TaskManager.lib.helpers.modules import create_module

import asyncio


async def main():
    module = await create_module(
        name='test',
        task_function=FC(func=test, timeout=4, retries=3, retry_delay=5),
        exc_function=FC(func=exc, timeout=5),
        threads=5
    )

    await create_task(module='test', account='account', logger=1, ff=3, hh7=6)

    await asyncio.sleep(5)
    module.threads = 3


async def test(account, logger, **kwargs):
    print(account, logger, kwargs)
    await asyncio.sleep(3)
    # raise Exception('hui')


async def exc(account, logger, **kwargs):
    print(account)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
