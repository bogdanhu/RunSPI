import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Selector")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.files = []

        # Label for displaying selected file count
        self.file_count_label = tk.Label(self, text="0 files selected")
        self.file_count_label.pack()

        # Listbox for displaying identified files
        self.files_treeview = ttk.Treeview(self, columns=("File", "Type","GEO"))
        self.files_treeview.pack(fill="both", expand=True)
        self.files_treeview.heading("#0", text="ID")
        self.files_treeview.heading("File", text="File")
        self.files_treeview.heading("Type", text="Type")
        self.files_treeview.heading("GEO", text="GEO")

        # Buttons for file operations
        open_files_button = tk.Button(self, text="Open Files", command=self.open_files)
        open_files_button.pack()

        select_all_button = tk.Button(self, text="Select All", command=self.select_all)
        select_all_button.pack()

        select_none_button = tk.Button(self, text="Select None", command=self.select_none)
        select_none_button.pack()

        # Run button for opening selected files
        run_button = tk.Button(self, text="Run", command=self.run)
        run_button.pack()

    def open_files(self):
        filetypes = (("STEP Files", "*.step;*.stp"), ("SLDPRT Files", "*.sldprt"), ("All Files", "*.*"))
        selected_files = filedialog.askopenfilenames(filetypes=filetypes)
        self.files_treeview.delete(*self.files_treeview.get_children())

        for file in selected_files:
            filename = os.path.basename(file)
            file_extension = os.path.splitext(filename)[1].lower()
            file_type = ""

            if file_extension in [".step", ".stp"]:
                file_type = "STEP"
            elif file_extension == ".sldprt":
                file_type = "SLDPRT"

            # Check if file with same name but different extension is already in the list
            existing_item = self.files_treeview.find_item(filename, "File")
            if existing_item:
                self.files_treeview.set(existing_item, "Type", file_type)
            else:
                self.files_treeview.insert("", "end", text=filename, values=(filename, file_type))

        self.update_file_count_label()

    def select_all(self):
        self.files_treeview.selection_set(self.files_treeview.get_children())

    def select_none(self):
        self.files_treeview.selection_clear(self.files_treeview.get_children())

    def run(self):
        selected_files = [self.files_treeview.item(item)["text"] for item in self.files_treeview.selection()]
        # Perform action with selected files, e.g. open in SolidWorks
        # Replace the following print statement with your desired action
        print("Opening files:", selected_files)

    def update_file_count_label(self):
        file_count = len(self.files_treeview.get_children())
        self.file_count_label.config(text=f"{file_count} files selected")


if __name__ == "__main__":
    app = Application()

    # Creăm fereastra principală a aplicației
   # root = tk.Tk()

    # Creăm o instanță a aplicației
    #app = Application(root)

    # Pornim bucla de evenimente a aplicației
    app.mainloop()