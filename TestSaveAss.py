import pygetwindow

def TestDialogConfirmareExists():
    from pywinauto.application import Application
    # Define the window title to check for
    window_title = "Confirmare"
    print("OK")
    # Connect to the SolidWorks application
    # Check if a window with the target title is found
    try:
        app = Application().connect(title_re=window_title)
        if app.window(title_re=window_title).exists():
            print(f"Window '{window_title}' is open.")
        else:
            print(f"Window '{window_title}' is not open.")
        return True
    except Exception as ex:
        print({ex})
        return False
        pass
        # Window not found, retry after a short delay

def FocusOnWindow(window_title="SolidWorks"):
    # Define the window title of SolidWorks
    # Get the SolidWorks window by title
    solidworks_window = pygetwindow.getWindowsWithTitle(window_title)
    # If the window is found, bring it to the front
    if solidworks_window:
        solidworks_window[0].activate()
    else:
        print(f"Window '{window_title}' not found.")


if __name__ == "__main__":
    FocusOnWindow()
    TestDialogConfirmareExists()
