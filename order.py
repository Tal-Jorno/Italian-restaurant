from typing import List
from uuid import UUID

import menu
from datetime import datetime
import threading


class OrderStatus:
    """Enum for order status."""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Order:
    _order_id: UUID
    _customer_name: str
    _order_date: str
    _finish_date: str
    _total_amount: float
    _dishes: List[menu.Dish]

    def __init__(self, order_id: UUID):
        self._order_id = order_id
        self._status = OrderStatus.PENDING
        self._total_amount = 0
        self._dishes = []
        self._lock = threading.Lock()

    def is_in_progress(self) -> bool:
        """Checks if the order is in progress."""
        with self._lock:
            return self._status == OrderStatus.IN_PROGRESS
        
    def is_pending(self) -> bool:
        """Checks if the order is pending."""
        with self._lock:
            return self._status == OrderStatus.PENDING

    def is_completed(self) -> bool:
        """Checks if the order is completed."""
        with self._lock:
            return self._status == OrderStatus.COMPLETED

    def is_cancelled(self) -> bool:
        """Checks if the order is cancelled."""
        with self._lock:
            return self._status == OrderStatus.CANCELLED

    def set_customer_name(self, name: str):
        """Sets the customer's name for the order."""
        with self._lock:
            self._customer_name = name

    def add_dish(self, dish: menu.Dish):
        """Adds a dish to the order and updates the total amount."""
        with self._lock:
            self._dishes.append(dish)
            self._total_amount += dish.price

    def remove_dish(self, dish: menu.Dish) -> bool:
        """Removes a dish from the order and updates the total amount."""
        with self._lock:
            if dish in self._dishes:
                self._dishes.remove(dish)
                self._total_amount -= dish.price
                return
            raise ValueError("dish not in list")

    def checkout(self):
        """Finalizes the order"""
        with self._lock:
            self._status = OrderStatus.IN_PROGRESS
            self._order_date = datetime.now().strftime("%Y-%m-%d")

    def complete(self):
        """Completes the order."""
        with self._lock:
            self._status = OrderStatus.COMPLETED
            self._finish_date = datetime.now().strftime("%Y-%m-%d")

    def cancel(self):
        """Cancels the order."""
        with self._lock:
            self._status = OrderStatus.CANCELLED
            self._order_date = datetime.now().strftime("%Y-%m-%d")

    def get_dishes(self) -> List[menu.Dish]:
        """Returns the list of dishes in the order."""
        with self._lock:
            return self._dishes

    def get_total_amount(self) -> float:
        """Returns the total amount of the order."""
        with self._lock:
            return self._total_amount

    def get_order_id(self) -> UUID:
        """Returns the order ID."""
        with self._lock:
            return self._order_id

    def get_customer_name(self) -> str:
        """Returns the customer's name."""
        with self._lock:
            return self._customer_name

    def __str__(self):
        """Returns a string representation of the order."""
        with self._lock:
            dishes_str = "\n".join([f"  - {dish.name}: ${dish.price}" for dish in self._dishes])
            return (
                f"Order ID: {self._order_id}\n"
                f"Customer: {self._customer_name}\n"
                f"Status: {self._status}\n"
                f"Total Amount: ${self._total_amount:.2f}\n"
                f"Dishes:\n{dishes_str}"
            )

    def __repr__(self):
        """Returns a string representation of the order."""
        with self._lock:
            dishes_str = "\n".join([f"  - {dish.name}: ${dish.price}" for dish in self._dishes])
            return (
                f"Order ID: {self._order_id}\n"
                f"Customer: {self._customer_name}\n"
                f"Status: {self._status}\n"
                f"Total Amount: ${self._total_amount:.2f}\n"
                f"Dishes:\n{dishes_str}"
            )
