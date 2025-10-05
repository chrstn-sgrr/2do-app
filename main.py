import tkinter as tk
from todo_app import TodoApp


def main():
    """
    Entry point for the 2do App.
    Creates the main Tkinter window and starts the application.
    """
    root = tk.Tk()  # Create main Tkinter window
    app = TodoApp(root)  # Instantiate TodoApp
    root.mainloop()  # Start tkinter event loop


if __name__ == "__main__":
    main()
