import threading
import queue
from typing import List
from order import Order
import uuid

from src.commands import CommandType, Command, \
    StopCommand, AcquireOrderCommand, OrderCommand, CommitOrderCommand, \
    CancelOrderCommand, DishCommand, ErrorResponse, AcquireOrderResponse, \
    GetOrderHistoryResponse, CommitOrderResponse, \
    CancelOrderResponse, GetOrderHistoryCommand, GetOrderCommand, GetOrderResponse, AddDishCommand, RemoveDishCommand, \
    SuccessResponse
from src.errors import BackendException
from src.menu import Dish


class Backend:
    def __init__(self):
        self._command_queue = queue.Queue()  # Thread-safe queue for commands
        self._response_queue = queue.Queue()  # Queue for responses
        self._active_orders = {}
        self._order_history = []  # List of all completed orders
        self._lock = threading.Lock()  # Lock for thread-safe operations
        self._running = True

        # Start the backend thread
        self._thread = threading.Thread(
            target=self._process_commands, daemon=True)
        self._thread.start()

    def _execute_command(self, command: Command):
        """Helper method to execute a command and return the response."""
        self._command_queue.put(command)
        response = self._response_queue.get()
        if isinstance(response, ErrorResponse):
            raise BackendException(response.error_message)
        return response

    def get_order(self, order_id: uuid.UUID) -> Order:
        """Get the order object for the given order ID."""
        response = self._execute_command(GetOrderCommand(order_id))
        return response.order

    def commit_order(self, order_id: uuid.UUID):
        """Create and commit an order."""
        response = self._execute_command(CommitOrderCommand(order_id))
        return response

    def cancel_order(self, order_id: uuid.UUID):
        """Cancel an order."""
        response = self._execute_command(CancelOrderCommand(order_id))
        return response

    def acquire_order(self, costumer_name: str) -> uuid.UUID:
        """Get the list of orders currently being prepared."""
        response: AcquireOrderResponse = self._execute_command(AcquireOrderCommand(costumer_name))
        return response.order_id

    def get_order_history(self) -> List[Order]:
        """Get the order history."""
        response = self._execute_command(GetOrderHistoryCommand())
        return response.order_history

    def add_dish(self, order_id: uuid.UUID, dish: Dish):
        """Add a dish to an order."""
        command = AddDishCommand(order_id,  dish)
        self._execute_command(command)

    def remove_dish(self, order_id: uuid.UUID, dish: Dish):
        """Remove a dish from an order."""
        command = RemoveDishCommand(order_id, dish)
        self._execute_command(command)

    def _process_commands(self):
        """Process commands from the queue."""
        while self._running:
            try:
                command = self._command_queue.get(timeout=1)
                response = None  # Initialize response variable
                if command.command_type == CommandType.STOP_COMMAND:
                    self._running = False
                elif command.command_type == CommandType.ACQUIRE_ORDER:
                    response = self._acquire_order(command.customer_name)

                elif command.command_type == CommandType.GET_ORDER_HISTORY:
                    with self._lock:
                        response = GetOrderHistoryResponse(
                            order_history=list(self._order_history))

                elif issubclass(type(command), OrderCommand):
                    order = self._active_orders.get(command.order)
                    if order is None:
                        raise BackendException("Order not found.")

                    if command.command_type == CommandType.GET_ORDER:
                        response = GetOrderResponse(order)
                    elif command.command_type == CommandType.COMMIT_ORDER:
                        response = self._commit_order(order)
                    elif command.command_type == CommandType.CANCEL_ORDER:
                        response = self._cancel_order(order)

                    elif isinstance(command, DishCommand):
                        if command.command_type == CommandType.ADD_DISH:
                            order.add_dish(command.dish)
                        elif command.command_type == CommandType.REMOVE_DISH:
                            try:
                                order.remove_dish(command.dish)
                            except ValueError:
                                raise BackendException("dish not found.")

                if response is not None:
                    self._response_queue.put(response)
                    continue
                self._response_queue.put(SuccessResponse)

            except BackendException as e:
                error_response = ErrorResponse(error_message=str(e))
                self._response_queue.put(error_response)

            except queue.Empty:
                continue

    def _commit_order(self, order: Order):
        """Commit an order and add it to the order history."""
        if order.get_order_id() in self._active_orders and order.is_pending():
            order.checkout()
            self._order_history.append(order)
            threading.Timer(300, self._complete_order, args=[order]).start()
            return CommitOrderResponse()
        raise BackendException('Order already committed')

    def _cancel_order(self, order: Order):
        """Cancel an order."""
        if order.get_order_id() in self._active_orders.keys() and not order.is_completed():
            order.cancel()
            self._order_history.append(order)
            return CancelOrderResponse()
        raise BackendException('Order already canceled')

    def _acquire_order(self, customer_name: str):
        """Acquire a new order."""
        order_id = uuid.uuid4()
        order = Order(order_id)
        order.set_customer_name(customer_name)
        self._active_orders[order_id] = order
        return AcquireOrderResponse(order_id)

    def _complete_order(self, order: Order):
        """Move an order from the active list to completed."""
        with self._lock:
            if order and order.is_in_progress():
                order.complete()
                self._active_orders.pop(order.get_order_id(), None)

    def stop(self):
        """Stop the backend thread."""
        self._execute_command(StopCommand())
        self._thread.join()
