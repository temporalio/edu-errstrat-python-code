import asyncio

from temporalio import activity


class HeartbeatActivities:

    @activity.defn
    async def greeting(self, name: str) -> str:
        activity.logger.info(f"Invoking the greeting activity with input: {input}")

        for x in range(0, 10):
            activity.heartbeat(x)
            activity.logger.info(f"Heartbeat: {x}")
            await asyncio.sleep(7)

        return f"Hello {name}"
