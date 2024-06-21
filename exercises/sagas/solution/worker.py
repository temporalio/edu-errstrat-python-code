import asyncio
import logging

from activities import PizzaOrderActivities
from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import PizzaOrderWorkflow


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    activities = PizzaOrderActivities()

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[PizzaOrderWorkflow],
        activities=[
            activities.get_distance,
            activities.send_bill,
            activities.process_credit_card,
            activities.notify_delivery_driver,
            activities.update_inventory,
            activities.revert_inventory,
            activities.refund_customer,
        ],
    )
    logging.info(f"Starting the worker....{client.identity}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())