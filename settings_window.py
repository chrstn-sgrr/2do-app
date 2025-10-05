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
        self.window.geometry("550x600")  # Increased size to show all elements
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
        
        # Create a frame to hold the canvas and scrollbar
        font_list_frame = tk.Frame(font_frame, bg=self.theme_colors["bg"], height=250)
        font_list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        font_list_frame.grid_propagate(False)  # Prevent frame from shrinking
        font_frame.grid_columnconfigure(1, weight=1)
        font_frame.grid_rowconfigure(0, weight=1)
        
        # Create canvas for custom font list with scrollbar
        canvas = tk.Canvas(font_list_frame, 
                          bg=self.theme_colors["entry_bg"],
                          highlightthickness=1,
                          highlightbackground=self.theme_colors["fg"])
        scrollbar = tk.Scrollbar(font_list_frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame inside canvas to hold font items
        font_items_frame = tk.Frame(canvas, bg=self.theme_colors["entry_bg"])
        canvas_window = canvas.create_window((0, 0), window=font_items_frame, anchor="nw")
        
        # Font families list
        self.font_families = ["TkDefaultFont", "Arial", "Helvetica", "Times New Roman", 
                        "Courier New", "Comic Sans MS", "Verdana", "Georgia", 
                        "Calibri", "Tahoma", "Trebuchet MS", "Lucida Console"]
        
        # Variable to track selected font
        self.font_var = tk.StringVar(value=self.settings["font_family"])
        
        # Create radio buttons for each font with preview
        self.font_buttons = []
        for font_name in self.font_families:
            # Create a frame for each font option
            font_option_frame = tk.Frame(font_items_frame, 
                                        bg=self.theme_colors["entry_bg"])
            font_option_frame.pack(fill=tk.X, pady=1)
            
            # Radio button with the font displayed in its own style
            try:
                rb = tk.Radiobutton(font_option_frame,
                                   text=font_name,
                                   variable=self.font_var,
                                   value=font_name,
                                   font=(font_name, 11),
                                   bg=self.theme_colors["entry_bg"],
                                   fg=self.theme_colors["fg"],
                                   activebackground=self.theme_colors["entry_bg"],
                                   activeforeground=self.theme_colors["fg"],
                                   selectcolor=self.theme_colors["button_bg"],
                                   anchor="w",
                                   highlightthickness=0)
            except:
                # If font doesn't exist, use default font
                rb = tk.Radiobutton(font_option_frame,
                                   text=f"{font_name} (not available)",
                                   variable=self.font_var,
                                   value=font_name,
                                   bg=self.theme_colors["entry_bg"],
                                   fg=self.theme_colors["fg"],
                                   activebackground=self.theme_colors["entry_bg"],
                                   activeforeground=self.theme_colors["fg"],
                                   selectcolor=self.theme_colors["button_bg"],
                                   anchor="w",
                                   highlightthickness=0)
            
            rb.pack(fill=tk.X, padx=5, pady=2)
            self.font_buttons.append(rb)
        
        # Update scroll region after adding all items
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Make canvas width match the frame width
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        font_items_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
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
        