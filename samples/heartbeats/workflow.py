import asyncio
from datetime import timedelta

from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import HeartbeatActivities


@workflow.defn
class HeartbeatWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info(f"HeartbeatWorkflow started with {input}")

        result = await workflow.execute_activity_method(
            HeartbeatActivities.greeting,
            name,
            start_to_close_timeout=timedelta(minutes=5),
            heartbeat_timeout=timedelta(seconds=10),
        )

        return f"The result is {result}"
