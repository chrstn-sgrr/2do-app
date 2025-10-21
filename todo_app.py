import tkinter as tk
import json
import os
from settings_window import SettingsWindow


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2do App")

        self.tasks = []  # List to store task dictionaries
        
        # Default settings
        self.settings = {
            "font_family": "TkDefaultFont",
            "font_size": 10,
            "dark_mode": False
        }

        self.load_settings()
        self.apply_theme()
        self.create_widgets()
        self.load_tasks()

    def priority_color(self, task):
        base = self.root.cget("bg")  # Get the default background color of the root window
        if self.settings["dark_mode"]:
            colors = {
                "normal": "#2b2b2b",       # Dark grey for normal priority in dark mode
                "medium": "#4a4420",       # Darker yellow for medium priority
                "high":   "#4a2a2a",       # Darker red for high priority
            }
        else:
            colors = {
                "normal": base,       # Normal priority tasks use the default background
                "medium": "#fff8c4",  # Light yellow for medium priority
                "high":   "#ffe4e4",  # Light red for high priority
            }
        # Return the color for the given priority, defaulting to 'normal' if not specified,
        # and falling back to 'base' if the priority is not in the colors map.
        return colors.get(task.get("priority", "normal"), base)

    def load_tasks(self):
        """
        Loads tasks from the 'data/tasks.json' file.
        If the file doesn't exist, it creates the directory and starts with an empty list.
        Handles cases where tasks are strings or missing the 'priority' key.
        """
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
                        # Convert old string-based tasks to dictionary format
                        self.tasks.append({"text": task, "completed": False, "priority": "normal"})
                    else:
                        # Ensure dictionary-based tasks have a priority key
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

    def load_settings(self):
        file_path = "data/settings.json"
        
        if not os.path.exists(file_path):
            print("Settings file not found. Using default settings.")
            return
        
        try:
            with open(file_path, "r") as file:
                loaded_settings = json.load(file)
                self.settings.update(loaded_settings)
        except json.JSONDecodeError:
            print("Invalid JSON data in settings file. Using default settings.")
    
    def save_settings(self):
        file_path = "data/settings.json"
        os.makedirs("data", exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(self.settings, file, indent=2)

    def apply_theme(self):
        if self.settings["dark_mode"]:
            bg_color = "#1e1e1e"
            fg_color = "#ffffff"
            entry_bg = "#2d2d2d"
            button_bg = "#3a3a3a"
        else:
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            entry_bg = "#ffffff"
            button_bg = "#e0e0e0"
        
        # Store theme colors for later use
        self.theme_colors = {
            "bg": bg_color,
            "fg": fg_color,
            "entry_bg": entry_bg,
            "button_bg": button_bg
        }
        
        # Apply to root window
        self.root.configure(bg=bg_color)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task = {"text": task_text, "completed": False, "priority": "normal"}
            self.tasks.append(task)
            self.create_task_checkbox(task, len(self.tasks) - 1)
            self.task_entry.delete(0, tk.END)  # Clear the input field

    def refresh_task_display(self):
        # Destroy all existing widgets in the tasks frame
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Recreate checkboxes for all current tasks
        for index, task in enumerate(self.tasks):
            self.create_task_checkbox(task, index)

    def remove_task(self):
        # Filter out completed tasks
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.refresh_task_display()

    def create_widgets(self):
        # Get theme colors and font
        font_config = (self.settings["font_family"], self.settings["font_size"])
        
        # Frame for task input elements
        input_frame = tk.Frame(self.root, bg=self.theme_colors["bg"])
        input_frame.pack(pady=10, fill=tk.X)

        self.task_entry = tk.Entry(input_frame, width=40, 
                                   bg=self.theme_colors["entry_bg"], 
                                   fg=self.theme_colors["fg"],
                                   font=font_config,
                                   insertbackground=self.theme_colors["fg"])
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.task_entry.bind("<Return>", self.on_enter_pressed)  # Bind Enter key to add_task
        self.root.bind("<Delete>", self.on_delete_pressed)     # Bind Delete key to remove_task

        # Frame to hold the individual task checkboxes
        self.tasks_frame = tk.Frame(self.root, bg=self.theme_colors["bg"])
        self.tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame for action buttons (remove, refresh, save)
        button_frame = tk.Frame(self.root, bg=self.theme_colors["bg"])
        button_frame.pack(pady=5, fill=tk.X)

        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task,
                              bg=self.theme_colors["button_bg"], 
                              fg=self.theme_colors["fg"],
                              font=font_config) 
        add_button.pack(side=tk.LEFT)

        # Settings button on the left side
        settings_button = tk.Button(button_frame, text="⚙ Settings", command=self.open_settings,
                                   bg=self.theme_colors["button_bg"], 
                                   fg=self.theme_colors["fg"],
                                   font=font_config)
        settings_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Remove Task/s", command=self.remove_task,
                                 bg=self.theme_colors["button_bg"], 
                                 fg=self.theme_colors["fg"],
                                 font=font_config)
        remove_button.pack(side=tk.LEFT, padx=5)

        refresh_button = tk.Button(button_frame, text="Refresh Tasks", command=self.refresh_task_display,
                                  bg=self.theme_colors["button_bg"], 
                                  fg=self.theme_colors["fg"],
                                  font=font_config)
        refresh_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks,
                               bg=self.theme_colors["button_bg"], 
                               fg=self.theme_colors["fg"],
                               font=font_config)
        save_button.pack(side=tk.LEFT, padx=5)

    def on_drag_start(self, event, index):
        self._drag_start_index = index

    def on_drag_stop(self, event):
        if not hasattr(self, "_drag_start_index"):
            return

        self.tasks_frame.update_idletasks()  # Ensure all widgets are updated for accurate positioning

        y = event.y_root  # Y-coordinate of the mouse release relative to the screen
        children = list(self.tasks_frame.winfo_children())  # Get all task rows
        target_index = len(children) - 1  # Default target to last position
        for i, w in enumerate(children):
            top = w.winfo_rooty()    # Absolute top Y-coordinate of the widget
            bottom = top + w.winfo_height()  # Absolute bottom Y-coordinate of the widget
            if y < bottom:
                target_index = i  # Found the target index if mouse is above the bottom of this widget
                break

        src = self._drag_start_index
        if 0 <= src < len(self.tasks) and target_index != src:
            task = self.tasks.pop(src)  # Remove task from its original position
            self.tasks.insert(target_index, task)  # Insert task at the new position
            self.refresh_task_display()  # Refresh the UI to reflect the new order

        del self._drag_start_index  # Clean up the stored index

    def create_task_checkbox(self, task, index):
        bg = self.priority_color(task)  # Get background color based on task priority
        font_config = (self.settings["font_family"], self.settings["font_size"])
        
        # Determine text color based on theme
        text_color = self.theme_colors["fg"]

        # Frame for the individual task row, colored by priority
        row = tk.Frame(self.tasks_frame, bg=bg)
        row.pack(fill=tk.X, padx=8, pady=2)

        # Drag handle (for reordering tasks)
        drag_handle = tk.Label(row, text="☰", bg=bg, fg=text_color, width=2, cursor="fleur")
        drag_handle.pack(side=tk.LEFT, padx=(0, 2), anchor="center")
        # Bind drag-and-drop to the drag handle
        drag_handle.bind("<Button-1>", lambda e, i=index: self.on_drag_start(e, i))
        drag_handle.bind("<ButtonRelease-1>", lambda e: self.on_drag_stop(e))

        # Colored box for priority indication
        priority_box = tk.Label(row, bg=bg, width=2, relief="ridge") 
        priority_box.pack(side=tk.LEFT, padx=(0, 5), anchor="center")
        # Bind left-click to show priority selection menu
        priority_box.bind("<Button-1>", lambda e, i=index: self.show_priority_menu(e, i))

        var = tk.BooleanVar(value=task["completed"])  # Boolean variable for checkbox state
        checkbox = tk.Checkbutton(
            row,
            text=task["text"], 
            variable=var,
            command=lambda: self.toggle_task(index),  # Command to toggle task completion
            bg=bg,
            fg=text_color,
            activebackground=bg,
            activeforeground=text_color,
            selectcolor=bg,
            highlightthickness=0,
            bd=0,
            anchor="w",
            font=font_config
        )
        checkbox.pack(fill=tk.X, anchor="w")

    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def on_enter_pressed(self, event):
        self.add_task()

    def on_delete_pressed(self, event):
        self.remove_task()

    def show_priority_menu(self, event, index):
        menu = tk.Menu(self.root, tearoff=0)  # Create a new menu without the tear-off feature
        priorities = ["normal", "medium", "high"]
        for p in priorities:
            color = self.priority_color({"priority": p})  # Get the color for the current priority
            menu.add_command(label=p.capitalize(), background=color, 
                             command=lambda priority=p: self.update_task_priority(index, priority))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)  # Display the menu at the cursor's absolute screen position
        finally:
            menu.grab_release() 

    def open_settings(self):
        SettingsWindow(self.root, self.settings, self.theme_colors, self.on_settings_applied)

    def on_settings_applied(self, new_settings):
        self.settings.update(new_settings)
        self.save_settings()
        self.apply_theme()
        
        # Recreate all widgets with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_widgets()
        self.refresh_task_display()

    def update_task_priority(self, index, new_priority):
        self.tasks[index]["priority"] = new_priority
        self.save_tasks() 
        self.refresh_task_display()

