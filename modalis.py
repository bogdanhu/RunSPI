import tkinter as tk


# Function to close the overlay window after a certain duration
def close_overlay(window):
    window.destroy()


# Function to show the overlay window
def show_overlay(message, duration=2000):
    print("overlay!")
    # Create the overlay window
    overlay = tk.Toplevel()
    overlay.wm_overrideredirect(True)  # Remove title bar and border
    overlay.wm_attributes("-topmost", True)  # Set window to be on top
    overlay.wm_attributes("-alpha", 0.7)  # Set window opacity (0.0-1.0)

    # Create a label to display the message
    label = tk.Label(overlay, text=message, bg='black', fg='white', font=('Helvetica', 12))
    label.pack(padx=10, pady=5)

    # Center the overlay window on the screen
    window_width = overlay.winfo_reqwidth()
    window_height = overlay.winfo_reqheight()
    screen_width = overlay.winfo_screenwidth()
    screen_height = overlay.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    overlay.geometry(f"+{x}+{y}")

    # Close the overlay window after the specified duration
    overlay.after(duration, lambda: close_overlay(overlay))




# Function to trigger showing the overlay window
def show_overlay_button():
    show_overlay("This is a notification!", duration=5000)


# Button to trigger showing the overlay window
if __name__=="__main__":
    # Create the Tkinter window
    root = tk.Tk()
    button = tk.Button(root, text="Show Overlay", command=show_overlay_button)
    button.pack()

    # Start the Tkinter event loop
    root.mainloop()
