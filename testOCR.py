import logging
from pywinauto import Desktop, mouse
import pyautogui
import time


def ScanForAssembly():
    global x, y

    from pywinauto import Application
    import time

    # Start SolidWorks
    app = Application().start(r"C:\Program Files\SolidWorks Corp\SolidWorks\SLDWORKS.exe")

    # Wait for SolidWorks window to be visible
    solidworks_window = None
    while solidworks_window is None:
        try:
            solidworks_window = app.window(title_re="SOLIDWORKS.*")
        except Exception as e:
            print("SolidWorks window not found. Retrying...")
            time.sleep(1)

    # Check for part loading completion
    while True:
        # Get the status bar text
        status_bar = solidworks_window.child_window(auto_id="1019", control_type="StatusBar")
        status_text = status_bar.texts()[0]

        # Check if part loading is complete
        if "Loading complete" in status_text:
            print("Part loading is complete.")
            break
        else:
            print("Waiting for part loading to complete...")
            time.sleep(1)



    # define the color to search for (in RGB format)
    color = (int('7D', 16), int('B2', 16), int('CE', 16))  # 7DB2CE
    # get the desktop object
    desktop = Desktop()
    tryCounter = 0
    # loop until the pixel is found
    AmdatClick = False
    while True:
        tryCounter += 1
        if tryCounter > 3:
            logging.info("Iesim ca nu gasim butonul de free geometry")
            break
        if AmdatClick:
            print("IES")
            break
        # capture the entire screen
        screenshot = pyautogui.screenshot()

        # search for the pixel color
        width, height = screenshot.size
        for x in range(width):

            for y in range(height):
                pixel_color = screenshot.getpixel((x, y))
                if pixel_color == color:
                    # move the mouse to the pixel position and click
                    print("OK")
                    logging.info(r"Am gasit butonul verde")
                    mouse.move((x, y))
                    mouse.click(coords=(x, y))
                    AmdatClick = True
                    break

            else:
                continue
            if AmdatClick:
                print("IES")
                break
        else:
            #print("NU AM GASIT NIMIC")
            # wait for 1 second before searching again
            time.sleep(1)
    return AmdatClick

if __name__=="__main__":
    print(ScanForAssembly())