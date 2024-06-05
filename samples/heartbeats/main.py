import asyncio
import sys

from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from workflow import HeartbeatWorkflow


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    # Execute a workflow
    handle = await client.start_workflow(
        HeartbeatWorkflow.run,
        "Mason",
        id="heartbeat-example",
        task_queue=TASK_QUEUE_NAME,
    )

    result = await handle.result()

    print(f"Result:\n {result}")


if __name__ == "__main__":
    asyncio.run(main())
