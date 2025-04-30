import dataclasses
from typing import Callable

import backend
from errors import BackendException
from menu import Menu
import json


class CLI:
    """Command Line Interface for the restaurant management system."""

    def __init__(self):
        self.current_order_id = None
        self.renew = False
        self.commands = {
            "show_menu": {
                "description": "Show the menu",
                "method": self.show_menu_command
            },
            "add_dish": {
                "description": "Add a dish to the menu",
                "method": self.add_dish_command
            },
            "remove_dish": {
                "description": "Remove a dish from the menu",
                "method": self.remove_dish_command
            },
            "list_history": {
                "description": "List the order history",
                "method": self.list_history_command
            },
            "commit_order": {
                "description": "Commit the current order",
                "method": self.commit_order_command
            },
            "cancel_order": {
                "description": "Cancel the current order",
                "method": self.cancel_order_command
            },
            "help": {
                "description": "Show help information",
                "method": self.show_help_command
            },
            "show_order": {
                "description": "Show the current order",
                "method": self.show_order_command
            }
        }
        self.server = backend.Backend()

    def show_menu_command(self):
        """Show the menu command."""
        menu = Menu.get_menu()
        print("Menu:")
        for category, dishes in menu:
            print(f"\n{category}:")
            for dish in dishes:
                print(f"- {dish.name} (${dish.price})")
                print(f"  Description: {dish.description}")

    def validate_category(self, category: str) -> str:
        """Validate that the category exists in the menu, ignoring case.

        Args:
            category (str): The category to validate.

        Returns:
            str: The correctly cased category name if valid.

        Raises:
            ValueError: If the category is not found.
        """
        menu = Menu.get_menu()
        for cat, _ in menu:
            if cat.lower() == category.lower():
                return cat
        print(f"Error: Category '{category}' not found.")
        raise ValueError(f"Invalid category: {category}")

    def add_dish_command(self):
        """Add a dish to the menu."""
        category = input("Enter category: ")
        try:
            category = self.validate_category(category)
        except ValueError:
            return

        dish_name = input("Enter dish name: ")
        dish_to_add = None
        menu = Menu.get_menu()
        for cat, dishes in menu:
            if cat == category:
                for dish in dishes:
                    if dish.name.lower() == dish_name.lower():
                        dish_to_add = dish
                        break
        if dish_to_add:
            try:
                self.server.add_dish(self.current_order_id, dish_to_add)
            except BackendException as e:
                print(f"Error adding dish: {e}")
                return
                
        else:
            print("Dish not found in the menu.")

    def remove_dish_command(self):
        """Remove a dish from the menu."""
        category = input("Enter category: ")
        try:
            category = self.validate_category(category)
        except ValueError:
            return

        dish_name = input("Enter dish name: ")
        dish_to_remove = None
        menu = Menu.get_menu()
        for cat, dishes in menu:
            if cat == category:
                for dish in dishes:
                    if dish.name.lower() == dish_name.lower():
                        dish_to_remove = dish
                        break
        if dish_to_remove:
            try:
                self.server.remove_dish(self.current_order_id, dish_to_remove)
            except BackendException as e:
                print(f"Error removing dish: {e}")
            
            print(f"Removed {dish_to_remove.name} from the order.")
        else:
            print("Dish not found in the menu.")

    def list_history_command(self):
        """List the order history."""
        history = self.server.get_order_history()
        print("Order History:")
        for order in history:
            print(order)

    def commit_order_command(self):
        """Commit the current order."""
        self.server.commit_order(self.current_order_id)
        self.renew = True
        print("Order committed successfully.")

    def cancel_order_command(self):
        """Cancel the current order."""
        self.renew = True
        self.server.cancel_order(self.current_order_id)
        print("Order canceled successfully.")

    def show_help_command(self):
        """Show help information."""
        print("Available commands:")
        for command, info in self.commands.items():
            print(f"- {command}: {info['description']}")


    def show_order_command(self):
        """Show the current order."""
        order = self.server.get_order(self.current_order_id)
        print(order)

    def run_command(self, command: str):
        """Run a command."""
        command = command.strip().lower()
        if command in self.commands:
            method = self.commands[command]["method"]
            if callable(method):
                method()
            else:
                print(f"Command '{command}' is not callable.")
        else:
            print(f"Unknown command: {command}. Type 'help' for a list of commands.")

    def start(self):
        while True:
            self.renew = False
            print("Hello!\nTo start, please enter your name (only alphabetic characters are allowed):\n")
            name = input().strip()

            # Validate customer name
            while not name.isalpha():
                print("Invalid name. Please enter a valid name (only alphabetic characters are allowed):")
                name = input().strip()

            self.current_order_id = self.server.acquire_order(name)

            print(f"Hello {name}, welcome to our restaurant!\n")
            print("Please enter a command (type 'help' for a list of commands):")
            command = input()
            while True:
                self.run_command(command)
                if self.renew:
                    break
                print("Please enter a command (type 'help' for a list of commands):")
                command = input()


if __name__ == "__main__":
    cli = CLI()
    cli.start()
