import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.exceptions import ActivityError, ApplicationError

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import PizzaOrderActivities
    from shared import Bill, CreditCardCharge, OrderConfirmation, PizzaOrder


@workflow.defn
class PizzaOrderWorkflow:
    @workflow.run
    async def order_pizza(self, order: PizzaOrder) -> OrderConfirmation:
        workflow.logger.info("Activity order_pizza workflow invoked")

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

        return confirmation
