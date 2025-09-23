from operator import iconcat
import tkinter as tk
import json
import os

class Dodo_App:

    def __init__(self, root):
        self.root = root
        self.root.title("2do App")
        self.root.iconbitmap("assets/favicon.ico")

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
                loaded_tasks = json.load(file)

                for task in loaded_tasks:
                    if isinstance(task, str):
                        self.tasks.append({"text": task, "completed":False})
                    else:
                        self.tasks.append(task)
                
                self.refresh_task_display()
        except json.JSONDecodeError:
            print("Invalid JSON data in json file. Starting with empty list")
    
    def save_tasks(self):
        file_path = "data/tasks.json"
        with open(file_path, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task = {"text": task_text, "completed":False}
            self.tasks.append(task)
            self.create_task_checkbox(task, len(self.tasks) - 1)
            self.task_entry.delete(0, tk.END)

    def on_enter_pressed(self, event):
        self.add_task()

    def refresh_task_display(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            self.create_task_checkbox(task, index)

    def remove_task(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.refresh_task_display()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", self.on_enter_pressed)

        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task) 
        add_button.pack(side=tk.LEFT)

        remove_button = tk.Button(button_frame, text="Remove Task/s", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Refresh Tasks", command=self.refresh_task_display)
        remove_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks)
        save_button.pack(side=tk.LEFT, padx=5)

    def create_task_checkbox(self, task, index):
        checkbox = tk.Checkbutton(
            self.tasks_frame,
            text=task["text"],
            variable=tk.BooleanVar(value=task["completed"]),
            command=lambda: self.toggle_task(index)
        )
        checkbox.pack(anchor="w", padx=10, pady=2)

    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]

if __name__ == "__main__":
    root = tk.Tk()
    app = Dodo_App(root)
    root.mainloop()