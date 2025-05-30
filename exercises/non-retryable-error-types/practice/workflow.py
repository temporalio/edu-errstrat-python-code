import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import PizzaOrderActivities
    from shared import Bill, CreditCardCharge, OrderConfirmation, PizzaOrder


@workflow.defn
class PizzaOrderWorkflow:
    @workflow.run
    async def order_pizza(self, order: PizzaOrder) -> OrderConfirmation:

        # TODO Part B: Set the type "CreditCardProcessingError" as a non-retryable error type
        # using the `non_retryable_error_types`` keyword argument. This argument takes a list.
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=15),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=160),
            maximum_attempts=100,
        )

        workflow.logger.info(f"Workflow order_pizza invoked")

        address = order.address

        total_price = 0
        for pizza in order.items:
            total_price += pizza.price

        distance = await workflow.execute_activity_method(
            PizzaOrderActivities.get_distance,
            address,
            start_to_close_timeout=timedelta(seconds=5),
        )

        if order.is_delivery and distance.kilometers > 25:
            error_message = "Customer lives outside the service area"
            workflow.logger.error(error_message)
            raise ApplicationError(error_message)

        workflow.logger.info(f"Distance is {distance.kilometers}")

        # Use a short timer duration here to simulate the passage of time
        # while avoiding delaying the exercise

        await asyncio.sleep(3)

        bill = Bill(
            customer_id=order.customer.customer_id,
            order_number=order.order_number,
            description="Pizza order",
            amount=total_price,
        )

        try:
            credit_card_charge = CreditCardCharge(
                bill=bill, credit_card=order.credit_card_info
            )
            # TODO Part B: Add the retry_policy to the execute_activity_method using the `retry_policy` keyword argument
            # TODO Part D: Add the heartbeat_timeout to the execute_activity_method using the `heartbeat_timeout` keyword argument
            credit_card_confirmation = await workflow.execute_activity_method(
                PizzaOrderActivities.process_credit_card,
                credit_card_charge,
                start_to_close_timeout=timedelta(seconds=5),
            )
        except ActivityError as e:
            workflow.logger.error(f"Unable to process credit card {e.message}")
            raise ApplicationError(
                "Unable to process credit card", "CreditCardProcessingError"
            )

        try:
            confirmation = await workflow.execute_activity_method(
                PizzaOrderActivities.send_bill,
                bill,
                start_to_close_timeout=timedelta(seconds=5),
            )
        except ActivityError as e:
            workflow.logger.error(f"Unable to bill customer {e.message}")
            raise ApplicationError("Unable to bill customer")

        # TODO PART C: Uncomment the code to run the Activity
        """
        delivery_driver_available = await workflow.execute_activity_method(
            PizzaOrderActivities.notify_delivery_driver,
            confirmation,
            start_to_close_timeout=timedelta(minutes=5),
            heartbeat_timeout=timedelta(seconds=10),
        )
        """

        if delivery_driver_available is not True:
            # Notify customer delivery is not available and they will have to come
            # get their pizza, or cancel the order and compensate.

            # For this exercise, change the value of the status variable to "DELIVERY FAILURE"
            confirmation.status = "DELIVERY FAILURE"

        return confirmation
