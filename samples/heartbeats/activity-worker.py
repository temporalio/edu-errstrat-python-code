import asyncio
import logging

from activities import HeartbeatActivities
from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    # Run the worker

    activities = HeartbeatActivities()

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        activities=[activities.greeting],
    )
    logging.info(f"Starting the Activity worker....{client.identity}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
