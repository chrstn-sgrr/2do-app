import tkinter as tk
import json
import os

class Dodo_App:

    def __init__(self, root):
        self.root = root
        self.root.title("2do App")

        self.tasks = []

        self.create_widgets()
        self.load_tasks()

    def load_tasks(self):
        file_path = "data/tasks.json"

        if not os.path.exists(file_path):
            print("JSON file not found. Starting with empty list")
            os.makedirs("data", exist_ok=True)
            return
        
        try:
            with open(file_path, "r") as file:
                self.tasks = json.load(file)
                for task in self.tasks:
                    self.tasks_listbox.insert(tk.END, task)
        except json.JSONDecodeError:
            print("Invalid JSON data in json file. Starting with empty list")
    
    def save_tasks(self):
        file_path = "data/tasks.json"
        with open(file_path, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.tasks_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def on_enter_pressed(self, event):
        self.add_task()

    def remove_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.tasks_listbox.delete(selected_index)

        except IndexError:
            print("No task selected to remove")

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", self.on_enter_pressed)

        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT)

        self.tasks_listbox = tk.Listbox(self.root, width=50, height=10)
        self.tasks_listbox.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks)
        save_button.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Dodo_App(root)
    root.mainloop()