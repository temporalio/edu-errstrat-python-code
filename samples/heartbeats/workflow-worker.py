import asyncio
import logging

from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import HeartbeatWorkflow


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[HeartbeatWorkflow],
    )
    logging.info(f"Starting the Workflow worker....{client.identity}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
