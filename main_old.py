import tkinter as tk
import json
import os

tasks = []

class task_actions: 

    def load_tasks():
        file_path = "data/tasks.json"
        if not os.path.exists(file_path):
            print("tasks.json not found.")
            return tasks
        
        try:
            with open(file_path, "r")as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON data.")
            return tasks

    def add_tasks():
        task_to_add = input()
        tasks.append(task_to_add)

    def remove_tasks():
        task_to_remove = input("Please enter which task to remove")
        try:
            tasks.remove(task_to_remove)
        except ValueError:
            print(f"{task_to_remove} does not exist, please try again.")

def gui(tasks_list):
    root = tk.Tk() # root = main window
    root.title("2do App")

    tasks_listbox = tk.Listbox(root)
    tasks_listbox.pack()

    for task in tasks_list:
        tasks_listbox.insert(tk.END, task)

    label = tk.Label(root, text="2-do List")
    label.pack()

    root.mainloop()

def main():

    global tasks
    tasks = task_actions.load_tasks()
    gui(tasks)

main()