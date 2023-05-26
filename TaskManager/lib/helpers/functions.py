import asyncio

from ...components.function import FunctionContainer as FC


async def async_initiator(func: callable, timeout: int | None, args: dict):
    if timeout:
        result = await asyncio.wait_for(
            func(**args), timeout=timeout
        )
    else:
        result, _ = await asyncio.wait(
            [func(**args)],
        )
        result = result.pop().result()

    return result


async def sync_initiator(func: callable, timeout: int | None, args: dict):
    if timeout:
        result = await asyncio.wait_for(
            asyncio.get_running_loop().run_in_executor(
                None,
                func,
                *list(args.values()),
            ),
            timeout=timeout,
        )
    else:
        result = await asyncio.get_running_loop().run_in_executor(
            None, func, *list(args.values())
        )

    return result


async def task_func_initiator(task_fc: FC, exc_fc: FC, args: dict) -> any:
    timeout = task_fc.timeout
    retries = task_fc.retries or 1
    retry_delay = task_fc.retry_delay or 0

    while retries:
        try:
            if task_fc.async_type:
                return await async_initiator(func=task_fc.func, timeout=timeout, args=args)

            else:
                return await sync_initiator(func=task_fc.func, timeout=timeout, args=args)

        except Exception as e:
            retries -= 1

            if exc_fc:
                await exc_func_initiator(exc_fc, args)

            if not retries:
                return e

        await asyncio.sleep(retry_delay)


async def exc_func_initiator(exc_fc: FC, args):
    if exc_fc.async_type:
        await async_initiator(func=exc_fc.func, timeout=exc_fc.timeout, args=args)

    else:
        await sync_initiator(func=exc_fc.func, timeout=exc_fc.timeout, args=args)
