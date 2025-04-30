#  Italian Restaurant - CLI Ordering System

This project is a command-line based ordering system for an Italian restaurant. It simulates the full process of menu navigation, dish selection, order management, and backend coordination using a thread-safe architecture.

---

##  Features

- View menu by category (Pizza, Spaghetti, Dessert)
- Add or remove dishes from your order
- Commit or cancel an order
- List all previous orders
- Interactive CLI for customer use
- Thread-safe backend processing using queues and threading
- Simulated delivery: orders are marked completed 5 minutes after commit

---

##  Project Structure

- `main.py` – Main CLI interface
- `menu.py` – Handles loading and structuring the menu from JSON
- `backend.py` – Thread-safe backend handling command execution and state
- `order.py` – Order object model with locking and status management
- `commands.py` – Command and response models for backend communication
- `menu.json` – Menu data (grouped by category)
- `errors.py` – Custom exception class for backend errors

---

##  How to Run

Make sure you're inside the `src` directory:

```bash
python main.py
