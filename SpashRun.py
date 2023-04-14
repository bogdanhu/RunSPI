import tkinter as tk
import threading
import time


class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My Application")
        self.geometry("300x200")

        self.splash_window = None  # Splash window object
        self.cancelled = False  # Flag to check if cancel button is pressed

        self.run_button = tk.Button(self, text="Run", command=self.start_function)
        self.run_button.pack(pady=10)

    def start_function(self):
        self.run_button.config(state=tk.DISABLED)  # Disable run button
        self.show_splash()  # Show splash window
        self.cancelled = False  # Reset cancel flag

        # Start a thread for the long-running function
        thread = threading.Thread(target=self.long_running_function)
        thread.start()

    def long_running_function(self):
        # Simulate a long-running function
        for i in range(10):
            if self.cancelled:
                break  # Exit the loop if cancel button is pressed
            time.sleep(1)

        # Close splash window after the function is complete
        self.hide_splash()
        self.run_button.config(state=tk.NORMAL)  # Enable run button

    def show_splash(self):
        self.splash_window = tk.Toplevel(self)
        self.splash_window.title("Splash")
        self.splash_window.geometry("200x100")

        splash_label = tk.Label(self.splash_window, text="Running...", font=("Helvetica", 14))
        splash_label.pack(pady=10)

        cancel_button = tk.Button(self.splash_window, text="Cancel", command=self.cancel_functions)
        cancel_button.pack()

        self.splash_window.transient(self)  # Set splash window as transient to the main window
        self.splash_window.grab_set()  # Grab focus to splash window
        self.update()  # Update the main window

    def hide_splash(self):
        if self.splash_window:
            self.splash_window.destroy()  # Close the splash window
            self.splash_window = None

    def cancel_function(self):
        self.cancelled = True  # Set cancel flag to True


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
