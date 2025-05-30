from dataclasses import dataclass
from typing import List

TASK_QUEUE_NAME = "pizza-tasks"


@dataclass
class Address:
    line1: str
    line2: str
    city: str
    state: str
    postal_code: str


@dataclass
class Bill:
    customer_id: int
    order_number: str
    description: str
    amount: int


@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    phone: str


@dataclass
class Distance:
    kilometers: int


@dataclass
class OrderConfirmation:
    order_number: str
    status: str
    confirmation_number: str
    billing_timestamp: int
    amount: int


@dataclass
class Pizza:
    description: str
    price: int


@dataclass
class CreditCardInfo:
    holderName: str
    number: str


@dataclass
class CreditCardCharge:
    bill: Bill
    credit_card: CreditCardInfo


@dataclass
class PizzaOrder:
    order_number: str
    customer: Customer
    items: List[Pizza]
    is_delivery: bool
    address: Address
    credit_card_info: CreditCardInfo


@dataclass
class CreditCardConfirmation:
    cardInfo: CreditCardInfo
    confirmationNumber: str
    amount: int
    billingTimestamp: int


def create_pizza_order() -> PizzaOrder:
    credit_card_info = CreditCardInfo(
        holderName="Lisa Anderson", number="4242424242424242"
    )
    customer = Customer(
        customer_id=8675309,
        name="Lisa Anderson",
        email="lisa@example.com",
        phone="555-555-0000",
    )
    address = Address(
        line1="741 Evergreen Terrace",
        line2="Apartment 221B",
        city="Albuquerque",
        state="NM",
        postal_code="87101",
    )
    pizza1 = Pizza(description="Large, with mushrooms and onions", price=1500)
    pizza2 = Pizza(description="Small, with pepperoni", price=1200)
    pizza3 = Pizza(description="Medium, with extra cheese", price=1300)

    pizza_list = [pizza1, pizza2, pizza3]

    pizza_order = PizzaOrder(
        order_number="XD001",
        customer=customer,
        items=pizza_list,
        is_delivery=True,
        address=address,
        credit_card_info=credit_card_info,
    )
    return pizza_order
