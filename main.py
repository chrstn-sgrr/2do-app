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

    def priority_color(self, task):
        base = self.root.cget("bg")
        colors = {
            "normal": base,
            "medium": "#fff8c4", 
            "high":   "#ffe4e4", 
        }
        return colors.get(task.get("priority", "normal"), base)

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
                        self.tasks.append({"text": task, "completed":False, "priority": "normal"})
                    else:
                        if "priority" not in task:
                            task["priority"] = "normal"
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
            task = {"text": task_text, "completed":False, "priority":self.priority_var.get()}
            self.tasks.append(task)
            self.create_task_checkbox(task, len(self.tasks) - 1)
            self.task_entry.delete(0, tk.END)

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
        input_frame.pack(pady=10, fill=tk.X)

        self.priority_var = tk.StringVar(value="normal")
        priority_menu = tk.OptionMenu(input_frame, self.priority_var, "normal","medium","high")
        priority_menu.pack(side=tk.LEFT, padx=5)

        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.task_entry.bind("<Return>", self.on_enter_pressed)
        self.root.bind("<Delete>", self.on_delete_pressed)

        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5, fill=tk.X)

        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task) 
        add_button.pack(side=tk.LEFT)

        remove_button = tk.Button(button_frame, text="Remove Task/s", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Refresh Tasks", command=self.refresh_task_display)
        remove_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks)
        save_button.pack(side=tk.LEFT, padx=5)

    def on_drag_start(self, event, index):
        self._drag_start_index = index

    def on_drag_stop(self, event):
        if not hasattr(self, "_drag_start_index"):
            return

        self.tasks_frame.update_idletasks()

        y = event.y_root
        children = list(self.tasks_frame.winfo_children())
        target_index = len(children) - 1
        for i, w in enumerate(children):
            top = w.winfo_rooty()
            bottom = top + w.winfo_height()
            if y < bottom:
                target_index = i
                break

        src = self._drag_start_index
        if 0 <= src < len(self.tasks) and target_index != src:
            task = self.tasks.pop(src)
            self.tasks.insert(target_index, task)
            self.refresh_task_display()

        del self._drag_start_index

    def create_task_checkbox(self, task, index):
        bg = self.priority_color(task)

        row = tk.Frame(self.tasks_frame, bg=bg)
        row.pack(fill=tk.X, padx=8, pady=2)

        var = tk.BooleanVar(value=task["completed"])
        checkbox = tk.Checkbutton(
            row,
            text=task["text"], 
            variable=var,
            command=lambda: self.toggle_task(index),
            bg=bg,
            activebackground=bg,
            selectcolor=bg,
            highlightthickness=0,
            bd=0,
            anchor="w"
        )
        checkbox.pack(fill=tk.X, anchor="w")

        row.bind("<Button-1>", lambda e, i=index: self.on_drag_start(e, i))
        row.bind("<ButtonRelease-1>", lambda e: self.on_drag_stop(e))
        checkbox.bind("<Button-1>", lambda e, i=index: self.on_drag_start(e, i))
        checkbox.bind("<ButtonRelease-1>", lambda e: self.on_drag_stop(e))

        row.configure(cursor="fleur")

    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def on_enter_pressed(self, event):
        self.add_task()

    def on_delete_pressed(self, event):
        self.remove_task()

if __name__ == "__main__":
    root = tk.Tk()
    app = Dodo_App(root)
    root.mainloop()