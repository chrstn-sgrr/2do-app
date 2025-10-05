import tkinter as tk


class SettingsWindow:
    def __init__(self, parent, current_settings, theme_colors, on_apply_callback):
        self.parent = parent
        self.settings = current_settings.copy()
        self.theme_colors = theme_colors
        self.on_apply_callback = on_apply_callback
        
        # Create the settings window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x450")
        self.window.configure(bg=theme_colors["bg"])
        
        # Make it a modal dialog
        self.window.transient(parent)
        self.window.grab_set()
        
        # Build the UI
        self._create_font_settings()
        self._create_theme_settings()
        self._create_buttons()
        self._create_credit_label()
    
    def _create_font_settings(self):
        # Font settings frame
        font_frame = tk.LabelFrame(self.window, text="Font Settings", 
                                  bg=self.theme_colors["bg"], 
                                  fg=self.theme_colors["fg"],
                                  font=(self.settings["font_family"], 10, "bold"))
        font_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Font family selection label
        tk.Label(font_frame, text="Font Family:", 
                bg=self.theme_colors["bg"], 
                fg=self.theme_colors["fg"]).grid(row=0, column=0, sticky="nw", padx=10, pady=5)
        
        # Create a frame to hold the listbox and scrollbar
        font_list_frame = tk.Frame(font_frame, bg=self.theme_colors["bg"])
        font_list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        font_frame.grid_columnconfigure(1, weight=1)
        font_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollbar for the font list
        font_scrollbar = tk.Scrollbar(font_list_frame)
        font_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox to display font previews
        self.font_listbox = tk.Listbox(font_list_frame, 
                                   height=10,
                                   bg=self.theme_colors["entry_bg"], 
                                   fg=self.theme_colors["fg"],
                                   selectbackground=self.theme_colors["button_bg"],
                                   selectforeground=self.theme_colors["fg"],
                                   yscrollcommand=font_scrollbar.set,
                                   exportselection=False)
        self.font_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        font_scrollbar.config(command=self.font_listbox.yview)
        
        # Font families list
        self.font_families = ["TkDefaultFont", "Arial", "Helvetica", "Times New Roman", 
                        "Courier New", "Comic Sans MS", "Verdana", "Georgia", 
                        "Calibri", "Tahoma", "Trebuchet MS", "Lucida Console"]
        
        # Add fonts to listbox with their own font preview
        selected_index = 0
        for i, font_name in enumerate(self.font_families):
            self.font_listbox.insert(tk.END, font_name)
            try:
                # Try to set each item to display in its own font
                self.font_listbox.itemconfig(i, font=(font_name, 11))
                if font_name == self.settings["font_family"]:
                    selected_index = i
            except:
                # If font doesn't exist, use default
                pass
        
        # Select the current font
        self.font_listbox.select_set(selected_index)
        self.font_listbox.see(selected_index)
        
        # Variable to track selected font
        self.font_var = tk.StringVar(value=self.settings["font_family"])
        
        # Update font_var when selection changes
        def on_font_select(event):
            selection = self.font_listbox.curselection()
            if selection:
                self.font_var.set(self.font_families[selection[0]])
        
        self.font_listbox.bind('<<ListboxSelect>>', on_font_select)
        
        # Font size selection
        tk.Label(font_frame, text="Font Size:", 
                bg=self.theme_colors["bg"], 
                fg=self.theme_colors["fg"]).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.size_var = tk.IntVar(value=self.settings["font_size"])
        size_spinbox = tk.Spinbox(font_frame, from_=8, to=24, textvariable=self.size_var,
                                 bg=self.theme_colors["entry_bg"], 
                                 fg=self.theme_colors["fg"],
                                 width=10)
        size_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    def _create_theme_settings(self):
        # Theme settings frame
        theme_frame = tk.LabelFrame(self.window, text="Theme Settings", 
                                   bg=self.theme_colors["bg"], 
                                   fg=self.theme_colors["fg"],
                                   font=(self.settings["font_family"], 10, "bold"))
        theme_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Dark mode checkbox
        self.dark_mode_var = tk.BooleanVar(value=self.settings["dark_mode"])
        dark_mode_check = tk.Checkbutton(theme_frame, text="Enable Dark Mode", 
                                        variable=self.dark_mode_var,
                                        bg=self.theme_colors["bg"], 
                                        fg=self.theme_colors["fg"],
                                        activebackground=self.theme_colors["bg"],
                                        activeforeground=self.theme_colors["fg"],
                                        selectcolor=self.theme_colors["entry_bg"])
        dark_mode_check.pack(padx=10, pady=10, anchor="w")
    
    def _create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.window, bg=self.theme_colors["bg"])
        button_frame.pack(pady=20)
        
        # Apply button
        apply_button = tk.Button(button_frame, text="Apply & Save", command=self._apply_settings,
                                bg=self.theme_colors["button_bg"], 
                                fg=self.theme_colors["fg"],
                                width=12)
        apply_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", command=self._cancel_settings,
                                 bg=self.theme_colors["button_bg"], 
                                 fg=self.theme_colors["fg"],
                                 width=12)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def _create_credit_label(self):
        credit_label = tk.Label(self.window, text="Dodo App by Christian Esguerra",
                               bg=self.theme_colors["bg"], 
                               fg=self.theme_colors["fg"],
                               font=(self.settings["font_family"], 9))
        credit_label.pack(pady=10)
    
    def _apply_settings(self):
        # Update settings dictionary
        new_settings = {
            "font_family": self.font_var.get(),
            "font_size": self.size_var.get(),
            "dark_mode": self.dark_mode_var.get()
        }
        
        # Call the callback function with new settings
        self.on_apply_callback(new_settings)
        
        # Close the window
        self.window.destroy()
    
    def _cancel_settings(self):
        self.window.destroy()

