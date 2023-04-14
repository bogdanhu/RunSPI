import os
from tkinter import *
import subprocess

class App:
    def __init__(self, master):
        self.master = master
        master.title("Aplicație de automatizare")

        # Crearea listei de fișiere
        self.file_list = []
        for file in os.listdir(r'D:\ANALIZA'):
            if file.endswith(".step") or file.endswith(".stp") or file.endswith(".sldprt"):
                self.file_list.append(file)

        # Crearea variabilei pentru butoanele Check All/None
        self.check_var = BooleanVar()
        self.check_var.set(True)

        # Crearea listei de variabile pentru fiecare fișier
        self.file_vars = []
        for file in self.file_list:
            var = BooleanVar()
            var.set(True)
            self.file_vars.append(var)

        # Crearea listei de Checkbuttons pentru fiecare fișier
        self.file_checks = []
        for i in range(len(self.file_list)):
            check = Checkbutton(master, text=self.file_list[i], variable=self.file_vars[i])
            check.grid(row=i+1, column=0, sticky=W)
            self.file_checks.append(check)

        # Crearea butoanelor Check All/None
        check_all = Checkbutton(master, text="Check All", variable=self.check_var, command=self.check_all_files)
        check_all.grid(row=0, column=0, sticky=W)
        check_none = Checkbutton(master, text="Check None", variable=self.check_var, command=self.check_none_files)
        check_none.grid(row=0, column=1, sticky=W)

        # Crearea butonului Run
        run_button = Button(master, text="Run", command=self.open_files)
        run_button.grid(row=len(self.file_list)+1, column=0, sticky=W)

    # Funcția pentru butonul Check All
    def check_all_files(self):
        for var in self.file_vars:
            var.set(True)

    # Funcția pentru butonul Check None
    def check_none_files(self):
        for var in self.file_vars:
            var.set(False)

    # Funcția pentru butonul Run
    def open_files(self):
        # Crearea listei de fișiere selectate
        selected_files = [self.file_list[i] for i in range(len(self.file_list)) if self.file_vars[i].get()]

        # Deschiderea fișierelor selectate în SolidWorks
        for file in selected_files:
            print('Running:')
            print(f'D:\ANALIZA\\{file}')
            # Continuați bucla for după ce combinația de tastatură a fost apăsată
            t = threading.Thread(target=asteapta_combinatie_tastatura)
            t.start()

            # Așteptați până când firul de execuție este terminat
            t.join()

            # Continuați bucla for după ce combinația de tastatură a fost apăsată
            print("Combinația de tastatură a fost apăsată!")

            os.system(f'D:\ANALIZA\\{file}')
            #subprocess.Popen([f'D:\ANALIZA\\{file}'])
            # Așteptați până când combinația de tastatură este apăsată
            #keyboard.wait(combinatie_tastatura)

            # Continuați bucla for după ce combinația de tastatură a fost apăsată
            print("Combinația de tastatură a fost apăsată!")
        print("Job Done")
# Crearea și rularea aplicației
root = Tk()
import keyboard
import threading

# Definiți combinația de tastatură pe care doriți să o așteptați
combinatie_tastatura = "ctrl+alt+c"
# Definiți o funcție pentru așteptarea combinației de tastatură într-un fir de execuție separat
def asteapta_combinatie_tastatura():
    keyboard.wait(combinatie_tastatura)
    print("Combinația de tastatură a fost apăsată!")

app = App(root)
root.mainloop()
