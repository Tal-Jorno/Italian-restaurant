from typing import List
from dataclasses import dataclass
import json


@dataclass
class Dish:
    """Class representing a dish in the menu.

    Attributes:
        name (str): The name of the dish.
        price (float): The price of the dish.
        description (str): A brief description of the dish.
    """

    name: str
    price: float
    description: str


class Menu:
    """Class representing a menu with a list of dishes grouped by categories.

    Attributes:
        categories (dict): A dictionary where keys are category names and values are lists of Dish objects.
    """

    _MENU_FILE = "./src/menu.json"
    _menu = []

    @staticmethod
    def get_menu() -> List[tuple[str, list[Dish]]]:
        """Returns the menu as a list of tuples,
        where each tuple contains a category name and a list of Dish objects.

        Returns:
            List[tuple[str, list[Dish]]]: A list of tuples containing category names and lists of Dish objects.
        """
        if not Menu._menu:
            Menu._load_from_json()
        return Menu._menu

    @staticmethod
    def _load_from_json() -> None:
        """Loads dishes grouped by categories from a JSON file."""
        try:
            with open(Menu._MENU_FILE, 'r') as file:
                data = json.load(file)
                for category, dishes in data.items():
                    Menu._menu.append((
                        category,
                        [
                            Dish(
                                name=dish['name'],
                                price=dish['price'],
                                description=dish['description']
                            )
                            for dish in dishes]))

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
