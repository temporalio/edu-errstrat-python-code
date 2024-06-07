import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import PizzaOrderActivities
    from shared import (
        Bill,
        CreditCardCharge,
        CreditCardProcessingError,
        OrderConfirmation,
        PizzaOrder,
    )


@workflow.defn
class PizzaOrderWorkflow:
    @workflow.run
    async def order_pizza(self, order: PizzaOrder) -> OrderConfirmation:

        # TODO Part B: Set the CreditCardProcessingException as a non-retryable error type
        # using the `non_retryable_error_types`` keyword argument. This argument takes a list.
        # Hint: To get the FQDN of the class name, use `CreditCardProcessingException.class.getName()
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=15),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=160),
            maximum_attempts=100,
        )

        workflow.logger.info(f"order_pizza workflow invoked")

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
            error_message = "customer lives outside the service area"
            workflow.logger.error(error_message)
            raise ApplicationError(error_message)

        workflow.logger.info(f"distance is {distance.kilometers}")

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
            # TODO Part B: Add the retryOptions to the ActivityOptions using the `retry_policy` keyword argument
            # TODO Part D: Add the HeartbeatTimeout to the ActivityOptions using the `heartbeat_timeout` keyword argument
            credit_card_confirmation = await workflow.execute_activity_method(
                PizzaOrderActivities.process_credit_card,
                credit_card_charge,
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=retry_policy,
                heartbeat_timeout=timedelta(seconds=10),
            )
        except ActivityError as e:
            workflow.logger.error("Unable to process credit card")
            raise ApplicationError(
                "Unable to process credit card", CreditCardProcessingError.__name__
            )

        try:
            confirmation = await workflow.execute_activity_method(
                PizzaOrderActivities.send_bill,
                bill,
                start_to_close_timeout=timedelta(seconds=5),
            )
        except ActivityError as e:
            workflow.logger.error("Unable to bill customer")
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
