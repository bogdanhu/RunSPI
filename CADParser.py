# https://www.youtube.com/watch?v=n5gItcGgIkk&ab_channel=JobinPy
#
import os
import sys
import tkinter as tk
import time
from tkinter import ttk
import win32clipboard
import pyautogui
import threading
import TestSaveAss

from modalis import show_overlay

import keyboard

# todo 3: sa pun bife, daca vreau sa se duca direct la unfold
# todo 0: sa se uite daca e assembly , si daca da sa nu incerce sa scoata unfold!
# todo 10: poate sa mearga la fiecare fisier si sa il salveze :?

combinatie_tastatura = "Ctrl+D"


def close_window():
    global running_flag,fereastra
    running_flag = False  # Set running_flag to False to signal threads to exit
    print("Ctrl+q detected. Closing!")
    mesaj = f'Inchidere de urgenta activata. Asteptati, eventual apasati Ctrl+D'
    print(mesaj)
    try:
        if fereastra:
            fereastra.destroy()
    except:
        print("Eroare la inchiderea ferestrei")
    fereastra = show_overlay2(mesaj,colorbg='red')
    root.cancel_function()
    keyboard.press_and_release("ctrl+D")
    # keyboard.send("ctrl+d")
    # root.destroy()


# Create a global flag variable to signal threads to exit
running_flag = True


def show_overlay2(message, duration=1000, destroy=False,colorbg='green',colorfg='white'):
    # Create the overlay window
    overlay = tk.Toplevel()
    overlay.wm_overrideredirect(True)  # Remove title bar and border
    overlay.wm_attributes("-topmost", True)  # Set window to be on top
    overlay.wm_attributes("-alpha", 0.6)  # Set window opacity (0.0-1.0)

    # Create a label to display the message
    label = tk.Label(overlay, text=message, bg=colorbg, fg=colorfg, font=('Helvetica', 12))
    label.pack(padx=10, pady=5)

    # Center the overlay window on the screen
    window_width = overlay.winfo_reqwidth()
    # print(f'Lungime: {window_width}')
    window_height = overlay.winfo_reqheight()
    screen_width = overlay.winfo_screenwidth()
    # print(f'Monitor: {screen_width}')
    screen_height = overlay.winfo_screenheight()
    x = (screen_width - window_width - 300)
    y = (screen_height - window_height - 0)
    overlay.geometry(f"+{x}+{y}")
    # Close the overlay window after the specified duration
    if duration > 2000:
        overlay.after(duration, lambda: overlay.destroy())

    if destroy == True:
        print("destroy")
        overlay.destroy()
    else:
        return overlay


class FisiereCAD:
    def __init__(self, numeFisier, cale):
        self.numeFisier = numeFisier
        self.cale = cale


class TreeViewEdit(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_list = []
        self.bind("<Double-1>", self.on_double_click)
        self.bind("<Double-1>", self.on_double_click)
        self.cell_widgets = {}

    def on_double_click(self, event):
        # idnetify the region
        region_clicked = self.identify_region(event.x, event.y)
        # print(region_clicked)
        if region_clicked not in ("tree", "cell"):
            return
        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1
        print(f'Column index:{column_index}')
        row = self.identify_row(event.y)
        selected_iid = self.focus()
        selected_values = self.item(selected_iid)
        try:
            if column == "#0":
                selected_text = selected_values.get("text")
            else:
                try:
                    selected_text = selected_values.get("values")[column_index]
                except Exception as ex:
                    print(f'{ex}')
        except IndexError:
            print("Parent click")
            return
        column_box = self.bbox(selected_iid, column)
        entry_edit = ttk.Entry(root, width=column_box[2])

        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)
        entry_edit.focus()
        entry_edit.bind("<FocusOut>", self.on_return)
        entry_edit.bind("<Return>", self.on_return)
        entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])
        print(f"Double-clicked on {region_clicked} with column number {column} and row {row}")
        print(selected_text)

    def on_return(self, event):
        print("OKKKK")
        new_text = event.widget.get()
        # ex I002

        selected_iid = event.widget.editing_item_iid
        # -1 (tree column) , 0 pt prima
        column_index = event.widget.editing_column_index
        print(f'Coloana: {column_index}')
        if column_index == -1:
            self.item(selected_iid, text=new_text)
        else:
            current_values = self.item(selected_iid).get("values")
            print(current_values)
            current_values[column_index] = new_text
            self.item(selected_iid, values=current_values)

        event.widget.destroy()

    def on_focus_out(self, event):
        event.widget.destroy()

    def list_files_recursive(self, directorul):
        """
        Recursively list files and directories in a given directory.
        """
        for item in os.listdir(directorul):
            # Get the full path of the item
            item_path = os.path.join(directorul, item)

            # Check if the item is a file
            if os.path.isfile(item_path):
                #print("File:", item_path)
                if item.lower().endswith(".step") or item.lower().endswith(".sldasm") or item.lower().endswith(
                        ".stp") or item.lower().endswith(".sldprt"):
                    if '~' in item.lower():
                        continue
                    print(f'File: {item.lower()}')
                    element = FisiereCAD(item, directorul)
                    self.file_list.append(element)
            # Check if the item is a directory
            elif os.path.isdir(item_path):
                pass
                #print("Directory:", item_path)

                # Recursively list files and directories in the subdirectory
                self.list_files_recursive(item_path)

    def add_checkbox(self, row, column, value):
        checkbox = ttk.Checkbutton(self, variable=value, command=lambda: self.on_checkbox_change(value, row, column))
        self._place_cell_widgets(row, column, checkbox)

    def on_checkbox_change(self, var, row, column):
        print("TRIGGER CHECKBOX!")
        new_value = var.get()
        current_values = self.item(row).get("values")
        current_values[column] = "Da" if new_value else "Nu"
        self.item(row, values=current_values)

    def on_combobox_select(self, event, row, column):
        print("TRIGGER!")
        new_value = event.widget.get()
        current_values = self.item(row).get("values")
        current_values[column] = new_value
        self.item(row, values=current_values)

    def add_combobox(self, row, column, value, values):
        combobox = ttk.Combobox(self, textvariable=value, values=values, state="readonly", width=10)
        combobox.bind("<<ComboboxSelected>>", lambda event: self.on_combobox_select(event, row, column))
        self._place_cell_widgets(row, column, combobox)

    def _place_cell_widgets(self, row, column, widget):
        x, y, width, height = self.bbox(row, column)
        widget.place(x=x, y=y, width=width, height=height)
        self.cell_widgets[(row, column)] = widget

    def get_widget(self, row, column):
        return self.cell_widgets.get((row, column))

    def open_files(self, folder=r'D:\Analiza'):
        filetypes = (("STEP Files", "*.step;*.stp"), ("SLDPRT Files", "*.sldprt"), ("All Files", "*.*"))
        # self.files_treeview.delete(*self.files_treeview.get_children())

        # Delete each item from the treeview
        for item in root.treeview_vehicles.get_children():
            print("STERGE")
            root.treeview_vehicles.delete(item)
        self.file_list = []

        self.list_files_recursive(folder)

        for index, element in enumerate(self.file_list):
            filename = os.path.basename(element.numeFisier)
            file_extension = os.path.splitext(filename)[1].lower()
            file_type = ""

            # Adăugați caseta de selectare pentru coloana "SheetMetal" și comboboxul pentru coloana "Material"
            sheet_metal_var = tk.BooleanVar(value=True)
            material_var = tk.StringVar(value="1.0038")
            materials = ["1.0038", "1.4301", "AlMg3"]
            geo_exists_var = tk.BooleanVar(value=False)

            if file_extension in [".step", ".stp"]:
                from StepHelper import is_assembly
                result = is_assembly(f'{element.cale}\\{filename}')
                #print(f'filename {filename} assembly status is {result}')
                if result:
                    sheet_metal_var.set(False)
                file_type = "STEP"
            elif file_extension == ".sldprt":
                file_type = "SLDPRT"

            if index % 2 == 0:

                sedan_row = root.treeview_vehicles.insert(parent="", index=tk.END,
                                                     values=(
                                                         filename, element.cale, material_var, sheet_metal_var, 1,
                                                         "NuX", "Nu", geo_exists_var),
                                                     text="BU", tags=('even_row',))
            else:
                sedan_row = root.treeview_vehicles.insert(parent="", index=tk.END,
                                                     values=(
                                                         filename, element.cale, material_var, sheet_metal_var, 1,
                                                         "NuX", "Nu", geo_exists_var),
                                                     text="BU", tags=('odd_row',))

            self.add_checkbox(sedan_row, 3, sheet_metal_var)
            self.add_combobox(sedan_row, 2, material_var, materials)
            self.add_checkbox(sedan_row, 7, geo_exists_var)
            # add_combobox(self, row, column, value, values):
            root.update()

        # self.update_file_count_label()


# Define a function to auto-select all rows
def select_all_rows():
    print("OK")
    for index, element in enumerate(root.treeview_vehicles.get_children()):
        print(f"try #{index}:{element}")
        root.treeview_vehicles.selection_add(element)


def apply_tag(item_id,status='selected'):
    # selected_item_id = treeview_vehicles.selection()[0]
    print(f"works for {item_id}")
    root.treeview_vehicles.selection_remove(item_id)  # Deselect the item
    root.treeview_vehicles.item(item_id, tags=(status,))
    root.update()  # Force update of GUI


def delete_items(_):
    print('Delete button detected')
    for i in root.treeview_vehicles.selection():
        datele = root.treeview_vehicles.item(i, "values")
        print(f"Stergem datele lui {datele}")
        root.treeview_vehicles.delete(i)


def on_button_click():
    global treeview_vehicles
    valoareFolder = root.AdresaEntry.get()
    print(f"Populam cu {valoareFolder}")
    root.treeview_vehicles.open_files(folder=valoareFolder)


def modifica_geofiles_recursive(directorul="", denumireFisier="cumSecheama", bucati=1):
    for item in os.listdir(directorul):
        # Get the full path of the item
        if 'old' in directorul:
            return
        item_path = os.path.join(directorul, item)

        # Check if the item is a file
        if os.path.isfile(item_path):
            if item.lower().endswith(".geo") and denumireFisier.lower() in item.lower():
                if '~' in item.lower():
                    continue
                print(f'Old File: {item.lower()} in {directorul}. Vrem {bucati} bucati noi')
                if bucati > 1:
                    new_filename = os.path.join(directorul, f'{denumireFisier}_{bucati}buc.geo')
                    os.rename(item_path, new_filename)
                    print(f'New File: {new_filename.lower()}')
        elif os.path.isdir(item_path):
            modifica_geofiles_recursive(item_path, denumireFisier, bucati=bucati)


def runMe():
    global running_flag,fereastra
    dimensiuneSelectie = len(root.treeview_vehicles.selection())
    fereastra = None
    popQuestion=False
    from tkinter import messagebox

    def confirm_exit():
        raspuns= messagebox.askyesno("Nu ai setat materialele.", " Vrei sa continui?")
        print(f'{raspuns}')
        return raspuns
    for index, item in enumerate(root.treeview_vehicles.selection()):
        datele = root.treeview_vehicles.item(item, "values")
        if 'PY_VAR' in datele[2]:
            popQuestion=True

    if popQuestion: # vine intrebarea
        print("Se pare ca nu a setat materialele")
        if not confirm_exit():
            print("Inchidem la selectia utilizatorului")

            try:
                close_window()


            except Exception as Ex:
                print(f"inchidem ferestrele {Ex}")
            try:
                root.hide_splash()
                fereastra.destroy()

            except Exception as Ex:
                print("Inchidem ")
            time.sleep(2)


    if root.cancelled:
        print("INCHID FUNCTIA")
        root.cancelled=False
        running_flag=True
        return

    for index, item in enumerate(root.treeview_vehicles.selection()):
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        # print(item)
        # Coloram cu verde fisierele parcurse
        mesaj = f'Continuam cu piesa.{index + 1}/{dimensiuneSelectie}\n Ctrl+Q && {combinatie_tastatura} pentru oprire de urgenta'
        apply_tag(item,'in_studystudy')
        print(mesaj)
        if fereastra:
            fereastra.destroy()
        fereastra = show_overlay2(mesaj)

        print("acum sa deschidem fisierul")
        dateRand = root.treeview_vehicles.item(item, "values")
        # SOLIDWORKS!

        os.system(f'\"{dateRand[1]}\\{dateRand[0]}\"')
        print("Selected Make: ", dateRand)
        keyboard.press_and_release('f')
        time.sleep(5)
        SalvareFisierCaSolidworks(dateRand)

        # Fa o poza
        try:
            SalveazaJPG(dateRand)
        except Exception as e:
            print(f'Eroare {e}')
        #
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        keyboard.press_and_release('s')
        keyboard.press_and_release('ctrl+a')
        keyboard.write(f'sheet metal wizard')
        time.sleep(2)
        keyboard.send('enter')
        time.sleep(2)
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()

        # Set the data to clipboard
        win32clipboard.SetClipboardText("test")

        # Close the clipboard
        win32clipboard.CloseClipboard()
        time.sleep(2)
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        for i in range(4):
            # Press the Tab key
            keyboard.press('tab')

            # Release the Tab key
            keyboard.release('tab')
            print(f"Pressed {i} tabs")
            time.sleep(0.1)

        TestareCampMaterial()
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        if '4301' in dateRand[2]:
            MaterialSkips = 1
            MaterialCauta = '304'
        elif '0038' in dateRand[2]:
            MaterialSkips = 0
            MaterialCauta = 's235jr'
        elif 'Al' in dateRand[2]:
            MaterialSkips = 2
            MaterialCauta = '5754'
        else:
            MaterialSkips = -1
        if MaterialSkips >= 0:
            SeteazaMaterialInSolidworks(MaterialCauta, MaterialSkips)
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        print(f"Valoreas pentru NoToolsVar este {root.NoToolsVar.get()}")
        if root.NoToolsVar.get():
            time.sleep(3)
            # print("bai!")
            keyboard.send('escape')
            keyboard.press_and_release('escape')
            keyboard.press_and_release('s')
            time.sleep(0.5)
            keyboard.press_and_release('s')
            keyboard.press_and_release('ctrl+a')
            keyboard.write(f'unfolding')
            time.sleep(2)
            keyboard.send('enter')
            print("TODO: trebuie sa facem si poza!")
        apply_tag(item)
        TestSaveAss.FocusOnWindow("Solidworks Premium")
        if root.cancelled:
            print("INCHID FUNCTIA")
            break
        mesaj = f'Astept dupa combinatia de tasta pentru continuare. {combinatie_tastatura}.\n Piesa {index + 1}/{dimensiuneSelectie}\n Ctrl+Q && {combinatie_tastatura} pentru oprire de urgenta'
        print(mesaj)
        if fereastra:
            fereastra.destroy()
        fereastra = show_overlay2(mesaj)
        root.update()
        if (index + 1) <= dimensiuneSelectie:  # pana la urma cred ca e mai bine sa fie si pentru ultima
            keyboard.wait(combinatie_tastatura)
        else:
            fereastra.destroy()
            fereastraX = show_overlay2("Ultima piesa.", duration=5000)
            root.update()
        if not running_flag:
            print("Trebuie sa oprim")
            running_flag = True
            break
        else:
            print("Combinația de tastatură a fost apăsată!")

        file_name = os.path.basename(dateRand[0])
        file_name_without_extension = os.path.splitext(file_name)[0]
        print(f'Fisier: {file_name_without_extension} cu bucati {dateRand[4]}')
        modifica_geofiles_recursive(directorul=root.AdresaEntry.get(), denumireFisier=file_name_without_extension,
                                    bucati=int(dateRand[4]))
        #
        # Perform action with selected files, e.g. open in SolidWorks
        # Replace the following print statement with your desired action
        # print("Opening files:", selected_files)
    if fereastra:
        fereastra.destroy()
    root.hide_splash()
    root.run_button.config(state=tk.NORMAL)  # Enable run button
    root.AdresaEntry.config(state=tk.NORMAL)
    print("Job Done!")

    #verificam daca exista oferta in directorul mare
    VerificaSiCreeazaOfertaDacaNuExista()

    root.cancelled=False #reset cancelled flag


def VerificaSiCreeazaOfertaDacaNuExista():
    if 'X:' in root.AdresaEntry.get():
        DirPrincipal = root.AdresaEntry.get().split('\\')[1]
        caleDir = f'X:\\{DirPrincipal}\\OFERTA'
        print(f'Director cercetat:{caleDir}')
        if os.path.exists(caleDir):
            print("Calea", caleDir, "există în sistemul de fișiere.")
        else:
            print("Calea", caleDir, "nu există în sistemul de fișiere. Il creez acum")
            try:
                os.makedirs(caleDir)
                print(f"Directorul {caleDir} a fost creat cu succes!")
            except:
                print("Avem o problema. Nu pot crea directorul")


def SalveazaJPG(dateRand):
    if not root.TakePhotoVar.get():
        print("Nu salvam poza")
        return
    import glob
    import os
    # Get the file name with extension from dateRand[0]
    file_name = dateRand[0]

    # Extract the file name without extension
    file_name_without_extension = os.path.splitext(file_name)[0]

    # Create the file pattern to search for files with the same filename but with .jpg extension
    file_pattern = os.path.join(dateRand[1], f"{file_name_without_extension}*.[jJ][pP][gG]")

    # Get a list of files in the current directory that match the file pattern
    matching_files = glob.glob(file_pattern)

    # Check if any matching file was found
    if matching_files:
        print(f"File with the same filename as '{file_name_without_extension}' but with .jpg extension exists in the same folder. Skipping saving!")
        return
    else:
        print(f"No file with the same filename as '{file_name_without_extension}' but with .jpg extension exists in the same folder.")


    print('salvez o poza pt {dateRand[0]}')
    keyboard.press_and_release('s')
    time.sleep(0.5)
    keyboard.write('save as', 0.1)
    time.sleep(2)
    keyboard.send('enter')
    time.sleep(0.5)
    keyboard.press_and_release('tab')  # sau ar merge si f4 !
    time.sleep(2)
    keyboard.press_and_release('j')
    time.sleep(0.5)
    keyboard.press_and_release('alt+s')
    time.sleep(0.5)
    print(f"Am salvat poza cu fisierul {dateRand[0]}")


def SalvareFisierCaSolidworks(dateRand):
    ###
    if '.stp' in dateRand[0].lower() or 'step' in dateRand[0].lower():
        # salveaza ca stp
        print('incerc sa salvez {dateRand[0]}')
        keyboard.press_and_release('s')
        time.sleep(0.5)
        keyboard.write('save')
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(0.5)
        keyboard.press_and_release('ctrl+L')  # sau ar merge si f4 !
        time.sleep(0.5)
        keyboard.write(dateRand[1], 0.1)
        time.sleep(1)
        keyboard.press_and_release('alt+s')
        time.sleep(1)

        if TestSaveAss.TestDialogConfirmareExists():
            keyboard.press('left')
            time.sleep(0.5)
            keyboard.press('enter')
            time.sleep(2)
        print(f"Am salvat fisierul {dateRand[0]} ca solidworks")
    ###


def SeteazaMaterialInSolidworks(MaterialCauta, MaterialSkips):
    for i in range(3):
        keyboard.press_and_release('up')
        time.sleep(1)
    for i in range(MaterialSkips):
        keyboard.press_and_release('down')
        time.sleep(1)
    keyboard.press_and_release('enter')
    time.sleep(2)
    keyboard.press_and_release('s')
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+a')
    keyboard.write(f'material edit')
    time.sleep(3)
    keyboard.send('enter')
    for i in range(5):
        # Press the Tab key
        keyboard.press('tab')

        # Release the Tab key
        keyboard.release('tab')
        print(f"Pressed {i} tabs")
        time.sleep(0.1)
    keyboard.write(MaterialCauta)
    time.sleep(0.3)
    keyboard.press_and_release('tab')
    time.sleep(0.2)
    keyboard.press_and_release('down')
    time.sleep(0.2)
    keyboard.press_and_release('down')
    time.sleep(0.2)
    keyboard.press_and_release('enter')
    time.sleep(0.2)
    keyboard.press_and_release('esc')
    time.sleep(0.5)
    ## File Properties Bucati
    # keyboard.press_and_release('enter')
    time.sleep(2)
    # keyboard.press_and_release('s')
    # time.sleep(0.5)
    # keyboard.press_and_release('ctrl+a')
    # keyboard.write(f'file properties')
    # time.sleep(2)
    # keyboard.send('enter')


def TestareCampMaterial():
    pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    win32clipboard.OpenClipboard()
    new_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    # print(new_data + ' duuuuude.')
    if "test" in new_data:
        # print("FAILED")
        keyboard.press_and_release('TAB')
        pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
        win32clipboard.OpenClipboard()
        new_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        # print(new_data + ' duuuuude.')
        if "test" in new_data:
            print("FAILED nasol!")
        else:
            print("GREAT x 2!")
    else:
        print("GREAT!")


def update_widget_positions(event):
    print("EVENT TRIGGER")
    if event.widget == root.treeview_vehicles:
        col = root.treeview_vehicles.identify_column(event.x)
        if col:
            col_index = int(col[1:]) - 1
            if col_index >= 0:
                for row in root.treeview_vehicles.get_children():
                    for column in range(9):  # treeview_vehicles["columns"]
                        widget = root.treeview_vehicles.get_widget(row, column)
                        if widget:
                            x, y, width, height = root.treeview_vehicles.bbox(row, column)
                            widget.place(x=x, y=y, width=width, height=height)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(tv, _col, not reverse))


def postPopUpMenu(event):
    row_id = root.treeview_vehicles.identify_row(event.y)
    root.treeview_vehicles.selection_set(row_id)
    row_values = root.treeview_vehicles.item(row_id)['values']
    print(row_values)
    popUpMenu = tk.Menu(root.treeview_vehicles, tearoff=0, font=("Verdana", 11))
    popUpMenu.add_command(label="Run it", command=root.start_function)
    popUpMenu.add_separator()
    popUpMenu.add_command(label="Delete it (neimplementat)", command=delete)
    popUpMenu.post(event.x_root, event.y_root)


def delete():
    print("deleting")

class CADApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1200x800")

        self.splash_window = None  # Splash window object
        self.cancelled = False  # Flag to check if cancel button is pressed
        self.AreYouSure=False #Flag for not setting material and continue
        self.label = tk.Label(self, text="Enter your location:")
        self.label.grid(row=0, column=0, sticky=tk.W)

        self.AdresaEntry = tk.Entry()
        self.AdresaEntry.grid(row=0, column=1, sticky=tk.W)  # Add the entry widget to the window
        self.AdresaEntry.bind("<Return>", lambda event: on_button_click())
        self.AdresaEntry.configure(font=('Helvetica', 16))

        # Create a button
        self.buttonAdresaEntry = tk.Button(self, text="Click me!", command=on_button_click)

        # Configure the button's background color
        self.buttonAdresaEntry.configure(bg='white', font=('Helvetica', 16))  # Set background color to blue
        # Configure the button's foreground color (text color)
        self.buttonAdresaEntry.configure(fg='green')  # Set text color to white

        self.buttonAdresaEntry.grid(row=0, column=2, sticky=tk.W)  # Add the button to the window
        print(self.AdresaEntry.get().strip())



        self.NoToolsVar = tk.BooleanVar()
        self.NoToolsVar.set(True)
        self.NoToolsSelection = tk.Checkbutton(self, text="No Tools", variable=self.NoToolsVar)
        self.NoToolsSelection.grid(row=1, column=0, sticky=tk.E)
        self.rowconfigure(1, minsize=20)

        self.TakePhotoVar = tk.BooleanVar()
        self.TakePhotoVar.set(True)
        self.TakePhotoVarSelection = tk.Checkbutton(self, text="Take Photos", variable=self.TakePhotoVar)
        self.TakePhotoVarSelection.grid(row=1, column=1, sticky=tk.W)

        column_name = (
        "DenumireCompleta", "CaleFisier", "Material", "SheetMetal", "NrBuc", "AreStp", "AreSldprt", "AreGeo")
        self.treeview_vehicles = TreeViewEdit(self, columns=column_name)

        # Define a tag for the selected row with desired appearance
        self.treeview_vehicles.tag_configure('selected', background='green', foreground='white')
        self.treeview_vehicles.tag_configure('even_row', background='#F0F0F0')
        self.treeview_vehicles.tag_configure('odd_row', background='#FFFFFF')
        self.treeview_vehicles.tag_configure('in_study', background='#FF0000')

        self.treeview_vehicles.heading("#0", text="PartID")
        self.treeview_vehicles.heading("DenumireCompleta", text="DenumireCompleta", anchor='w')
        self.treeview_vehicles.heading("CaleFisier", text="Cale Fisier")
        self.treeview_vehicles.heading("Material", text="Material")
        self.treeview_vehicles.heading("SheetMetal", text="SheetMetal")
        self.treeview_vehicles.heading("AreStp", text="AreStp")
        self.treeview_vehicles.heading("AreSldprt", text="AreSldprt")
        self.treeview_vehicles.heading("AreGeo", text="GEO")
        self.treeview_vehicles.heading("NrBuc", text="Numar Bucati")

        for col in column_name:
            self.treeview_vehicles.heading(col, text=col, command=lambda _col=col: \
                root.treeview_sort_column(self.treeview_vehicles, _col, False))

        # Populate
        #  treeview_vehicles.open_files()
        self.treeview_vehicles.column("DenumireCompleta", minwidth=400)
        self.treeview_vehicles.column("CaleFisier", width=100)
        self.treeview_vehicles.column("Material", width=10)
        self.treeview_vehicles.column("SheetMetal", width=10)
        self.treeview_vehicles.column("NrBuc", width=15)
        self.treeview_vehicles.column("AreGeo", width=10)
        self.treeview_vehicles.column("AreSldprt", width=10)
        self.treeview_vehicles.column("AreStp", width=10)
        self.treeview_vehicles.column("#0", width=30)

        # treeview_vehicles.insert(parent=sedan_row, index=tk.END, values=("Dacia", "2010", "Gri"))
        self.treeview_vehicles.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        self.treeview_vehicles.columnconfigure(0,
                                          weight=1)  # Make the Treeview widget expand horizontally to fill the entire column

        self.treeview_vehicles.bind("<Return>", lambda event: runMe())
        self.rowconfigure(2, weight=1, minsize=500)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # Create a button to trigger the auto-select function
        select_all_button = tk.Button(self, text='Select All', command=select_all_rows)
        select_all_button.config(font=('Helvetica', 16), bg='white', fg='red')
        select_all_button.grid(row=3, column=0, sticky=tk.E)

        # sa tina legatura cu widgeturile modificate dinamic
        self.treeview_vehicles.bind("<Configure>", lambda event: update_widget_positions(event))
        self.treeview_vehicles.bind("<ButtonRelease-1>", lambda event: update_widget_positions(event))
        self.treeview_vehicles.bind("<Button-3>", lambda event: postPopUpMenu(event))

        # Bind the Treeview widget to the '<<TreeviewSelect>>' event
        # and call the function to apply tag to the selected item
        # treeview_vehicles.bind('<<TreeviewSelect>>', apply_tag)

        self.treeview_vehicles.bind('<Delete>', delete_items)
        # Crearea butonului Run

        self.run_button = tk.Button(self, text="Run", command=self.start_function)
        self.run_button.grid(row=3, column=1, sticky=tk.W)
        self.run_button.config(font=('Helvetica', 16), bg='white', fg='green')
        self.title("CAD PARSER & Automation @ HELPAN 2023")

    def start_function(self):
        self.run_button.config(state=tk.DISABLED)  # Disable run button
        self.AdresaEntry.config(state=tk.DISABLED)
        self.show_splash()  # Show splash window
        self.cancelled = False  # Reset cancel flag

        # Start a thread for the long-running function
        self.thread = threading.Thread(target=runMe)
        self.thread.start()

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

        self.splash_label = tk.Label(self.splash_window, text="Running...", font=("Helvetica", 14))
        self.splash_label.pack(pady=10)

        cancel_button = tk.Button(self.splash_window, text="Cancel", command=self.cancel_function)
        cancel_button.pack()

        self.splash_window.transient(self)  # Set splash window as transient to the main window
        self.splash_window.grab_set()  # Grab focus to splash window
        self.update()  # Update the main window

    def hide_splash(self):
        if self.splash_window:
            self.splash_window.destroy()  # Close the splash window
            self.splash_window = None

    def cancel_function(self):
        print("Cancelling process")
        self.splash_label.configure(text= "INCHIDEM FUNCTIA. Asteptati va rog")
        self.cancelled = True  # Set cancel flag to True
        self.splash_window.update()
        print("BEFORE JOIN")
        try:
            self.thread.join(timeout=3)
            self.hide_splash()
        except:
            print("erori prin join")
        self.run_button.config(state=tk.NORMAL)  # Enable run button
        self.run_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = CADApp()
    # denumire_completa
    # daca are step
    # daca are sldprt
    # daca are geo
    # material
    # nrbuc









    # sedan_row = treeview_vehicles.insert(parent="", index=tk.END, text="SEDAN")


    keyboard.add_hotkey('ctrl+q', close_window)


    datafile = "cad-icon.ico"
    if not hasattr(sys, "frozen"):
        datafile = os.path.join(os.path.dirname(__file__), datafile)
    else:
        datafile = os.path.join(sys.prefix, datafile)

    root.iconbitmap(default=resource_path(datafile))
    root.mainloop()
