import customtkinter as ctk
from text_engine import TextEngine  # <--- IMPORT THE BRAIN
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class CodeEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Setup Window
        self.title("PyEdit - Python Code Editor")
        self.geometry("900x600") # Made it slightly wider for the sidebar

        # Layout: 2 Columns. 
        # Column 0 = Sidebar (Fixed width)
        # Column 1 = Editor (Expandable)
        self.grid_columnconfigure(0, weight=0) # Sidebar doesn't expand
        self.grid_columnconfigure(1, weight=1) # Editor expands
        self.grid_rowconfigure(0, weight=1)

        self.engine = TextEngine()

        # 2. Create Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # 3. Sidebar Buttons
        self.btn_open = ctk.CTkButton(self.sidebar, text="Open File", command=self.open_file)
        self.btn_open.pack(pady=10, padx=10)

        self.btn_save = ctk.CTkButton(self.sidebar, text="Save File", command=self.save_file)
        self.btn_save.pack(pady=10, padx=10)

        # 4. Create Editor Display
        self.display_label = ctk.CTkLabel(
            self, 
            text="Start typing...", 
            font=("Consolas", 16), 
            anchor="nw", 
            justify="left",
            fg_color="#1e1e1e",
            text_color="white"
        )
        self.display_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 5. Bind Keys
        self.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        """
        Receives the key event, sends it to the engine, and updates the UI.
        """
        # DEBUG: See what is happening
        print(f"Key sym: {event.keysym}, Char: '{event.char}'")

        # 1. Handle Backspace
        if event.keysym == "BackSpace":
            self.engine.delete_char()
            self.redraw()
            return
            
        # 2. Handle Return (Enter)
        if event.keysym == "Return":
            self.engine.insert_char("\n")
            self.redraw()
            return

        # 3. Handle Left Arrow (MUST BE BEFORE empty char check)
        if event.keysym == "Left":
            new_pos = self.engine.cursor_pos - 1
            self.engine.set_cursor(new_pos)
            self.redraw()
            return

        # 4. Handle Right Arrow (MUST BE BEFORE empty char check)
        if event.keysym == "Right":
            new_pos = self.engine.cursor_pos + 1
            self.engine.set_cursor(new_pos)
            self.redraw()
            return

        # 5. NOW we can safely ignore modifiers (Shift, Ctrl, Alt)
        if event.char == "": 
            return
        
        # 6. Handle Normal Characters
        self.engine.insert_char(event.char)
        self.redraw()

    def redraw(self):
        """
        Gets the text from the engine and paints it on the label.
        """
        full_text = self.engine.get_text()
        self.display_label.configure(text=full_text)

    def open_file(self):
        # 1. Ask user for path
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if not filepath:
            return # User cancelled

        # 2. Open and Read
        with open(filepath, "r") as f:
            content = f.read()

        # 3. Load into Engine
        self.engine.load_text(content)
        self.redraw()
        self.title(f"PyEdit - {filepath}")

    def save_file(self):
        # 1. Ask user for path
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if not filepath:
            return # User cancelled

        # 2. Get text from Engine
        content = self.engine.get_text().replace("|", "") # Remove cursor before saving

        # 3. Write to file
        with open(filepath, "w") as f:
            f.write(content)
        
        self.title(f"PyEdit - {filepath}")


if __name__ == "__main__":
    app = CodeEditorApp()
    app.mainloop()