from time import time

from shared import (
    Address,
    Bill,
    CreditCardCharge,
    CreditCardConfirmation,
    CreditCardProcessingError,
    Distance,
    InvalidChargeAmountError,
    OrderConfirmation,
)
from temporalio import activity
from temporalio.exceptions import ApplicationError


class PizzaOrderActivities:
    @activity.defn
    async def get_distance(self, address: Address) -> Distance:
        activity.logger.info(
            "get_distance invoked; determining distance to customer address"
        )

        # This is a simulation, which calculates a fake (but consistent)
        # distance for a customer address based on its length. The value
        # will therefore be different when called with different addresses,
        # but will be the same across all invocations with the same address.

        kilometers = len(address.line1) + len(address.line2) - 10
        if kilometers < 1:
            kilometers = 5

        distance = Distance(kilometers=kilometers)

        activity.logger.info(f"get_distance complete: {distance}")
        return distance

    @activity.defn
    async def send_bill(self, bill: Bill) -> OrderConfirmation:
        activity.logger.info(
            f"send_bill invoked: customer: {bill.customer_id} amount: {bill.amount}"
        )

        charge_amount = bill.amount

        if charge_amount > 3000:
            activity.logger.info("applying discount")

            charge_amount -= 500

        if charge_amount < 0:
            error_message = f"invalid charge amount: {charge_amount}"
            activity.logger.error(error_message)

            raise ApplicationError(
                error_message,
                type=InvalidChargeAmountError.__name__,
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
                type=CreditCardProcessingError.__name__,
                non_retryable=True,
            )
