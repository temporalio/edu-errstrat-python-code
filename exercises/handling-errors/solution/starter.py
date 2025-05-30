import asyncio
import logging

from shared import TASK_QUEUE_NAME, create_pizza_order
from temporalio.client import Client
from workflow import PizzaOrderWorkflow

logging.basicConfig(level=logging.INFO)


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    order = create_pizza_order()

    # Execute a workflow
    handle = await client.start_workflow(
        PizzaOrderWorkflow.order_pizza,
        order,
        id=f"pizza-workflow-order-{order.order_number}",
        task_queue=TASK_QUEUE_NAME,
    )

    result = await handle.result()

    logging.info(f"Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
