import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List

from src.menu import Dish
from src.order import Order


class CommandType(Enum):
    """Enum for command types."""
    GET_ORDER = "get_order"
    COMMIT_ORDER = "commit_order"
    ACQUIRE_ORDER = "acquire_order"
    GET_ORDER_HISTORY = "get_order_history"
    ADD_DISH = "add_dish"
    REMOVE_DISH = "remove_dish"
    CANCEL_ORDER = "cancel_order"
    STOP_COMMAND = "stop_command"


class Command:
    """Class representing a command to be executed."""
    command_type: CommandType


class StopCommand(Command):
    """Class representing a command to stop the backend."""

    def __init__(self):
        self.command_type: CommandType = CommandType.STOP_COMMAND


class AcquireOrderCommand(Command):
    def __init__(self, customer_name: str):
        self.command_type: CommandType = CommandType.ACQUIRE_ORDER
        self.customer_name = customer_name


class GetOrderHistoryCommand(Command):
    def __init__(self):
        self.command_type: CommandType = CommandType.GET_ORDER_HISTORY


class OrderCommand(Command):
    """Class representing a command to be executed on an order."""
    order: uuid.UUID

    def __init__(self, order: uuid.UUID):
        self.order = order


class GetOrderCommand(OrderCommand):
    def __init__(self, order_id: uuid.UUID):
        self.command_type: CommandType = CommandType.GET_ORDER
        super().__init__(order_id)


class CommitOrderCommand(OrderCommand):
    """Class representing a command to commit an order."""

    def __init__(self, order_id: uuid.UUID):
        self.command_type: CommandType = CommandType.COMMIT_ORDER
        super().__init__(order_id)


class CancelOrderCommand(OrderCommand):
    """Class representing a command to cancel an order."""

    def __init__(self, order_id: uuid.UUID):
        self.command_type: CommandType = CommandType.CANCEL_ORDER
        super().__init__(order_id)


class DishCommand(OrderCommand):
    """Class representing a command to be executed on a
    dish."""
    dish: Dish

    def __init__(self, order_id: uuid.UUID, dish: Dish):
        self.dish = dish
        super().__init__(order_id)


class AddDishCommand(DishCommand):
    """Class representing a command to add a dish to an order."""

    def __init__(self, order_id: uuid.UUID, dish: Dish):
        self.command_type: CommandType = CommandType.ADD_DISH
        super().__init__(order_id, dish)


class RemoveDishCommand(DishCommand):
    """Class representing a command to remove a dish from an order."""

    def __init__(self, order_id: uuid.UUID, dish: Dish):
        self.command_type: CommandType = CommandType.REMOVE_DISH
        super().__init__(order_id, dish)


class Response:
    """Base class for all responses."""
    pass


@dataclass
class ErrorResponse(Response):
    """Class representing an error response."""
    error_message: str


class SuccessResponse(Response):
    pass


@dataclass
class AcquireOrderResponse(SuccessResponse):
    """Class representing a response to acquire an order."""
    order_id: uuid.UUID


@dataclass
class GetOrderHistoryResponse(SuccessResponse):
    """Class representing a response to get order history."""
    order_history: List[Order]


@dataclass
class CommitOrderResponse(SuccessResponse):
    """Class representing a response to commit an order."""
    pass

@dataclass
class GetOrderResponse(SuccessResponse):
    """Class representing a response to get an order."""
    order: Order

@dataclass
class CancelOrderResponse(SuccessResponse):
    """Class representing a response to cancel an order."""
    pass
