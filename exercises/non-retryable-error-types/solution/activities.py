import asyncio
import random
from time import time

from shared import (
    Address,
    Bill,
    CreditCardCharge,
    CreditCardConfirmation,
    Distance,
    OrderConfirmation,
)
from temporalio import activity
from temporalio.exceptions import ApplicationError


class PizzaOrderActivities:
    @activity.defn
    async def get_distance(self, address: Address) -> Distance:
        activity.logger.info(
            "Activity get_distance invoked; determining distance to customer address"
        )

        # This is a simulation, which calculates a fake (but consistent)
        # distance for a customer address based on its length. The value
        # will therefore be different when called with different addresses,
        # but will be the same across all invocations with the same address.

        kilometers = len(address.line1) + len(address.line2) - 10
        if kilometers < 1:
            kilometers = 5

        distance = Distance(kilometers=kilometers)

        activity.logger.info(f"Activity get_distance complete: {distance}")
        return distance

    @activity.defn
    async def send_bill(self, bill: Bill) -> OrderConfirmation:
        activity.logger.info(
            f"Activity send_bill invoked: customer: {bill.customer_id} amount: {bill.amount}"
        )

        charge_amount = bill.amount

        if charge_amount > 3000:
            activity.logger.info("Applying discount")

            charge_amount -= 500

        if charge_amount < 0:
            error_message = f"Invalid charge amount: {charge_amount}"
            activity.logger.error(error_message)

            raise ApplicationError(
                error_message,
                type="InvalidChargeAmountError",
                non_retryable=True,
            )

        confirmation = OrderConfirmation(
            order_number=bill.order_number,
            status="SUCCESS",
            confirmation_number="P24601",
            billing_timestamp=time(),
            amount=charge_amount,
        )

        return confirmation

    @activity.defn
    async def process_credit_card(
        self, charge_info: CreditCardCharge
    ) -> CreditCardConfirmation:
        if len(charge_info.credit_card.number) == 16:
            card_processing_confirmation_number = "PAYME-78759"
            return CreditCardConfirmation(
                cardInfo=charge_info.credit_card,
                confirmationNumber=card_processing_confirmation_number,
                amount=charge_info.bill.amount,
                billingTimestamp=int(time()),
            )
        else:
            raise ApplicationError(
                "Invalid credit card number",
                type="CreditCardProcessingError",
            )

    @activity.defn
    async def notify_delivery_driver(self, order: OrderConfirmation) -> bool:
        """
        This is a simulation of attempting to notify a delivery driver that
        the order is ready for delivery. It starts by generating a number from 0 - 14.
        From there a loop is iterated over from 0 < 10, each time checking to
        see if the random number matches the loop counter and then sleeping for 5
        seconds. Each iteration of the loop sends a heartbeat back letting the
        Workflow know that progress is still being made. If the number matches a
        loop counter, it is a success. If it doesn't, then a delivery driver was
        unable to be contacted and failure is returned.
        """
        success_simulation = random.randint(0, 14)

        for x in range(10):
            if success_simulation == x:
                # Pretend to use the `order` variable to notify the driver
                activity.logger.info("Delivery driver responded")
                return True

            # Assuming Activity.getExecutionContext().heartbeat is a valid function call in your context
            activity.heartbeat(f"Heartbeat: {x}")
            activity.logger.info(f"Heartbeat: {x}")

            await asyncio.sleep(15)

        activity.logger.info("Delivery driver didn't respond")
        return False
