from tkinter import messagebox
import tkinter as tk
import csv

class App:
    def __init__(self):
        self.root = tk.Tk()
       # Gets the requested values of the height and widht.
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        
        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight-250, positionDown-80))
        self.root.title("Menu")
        self.name = ''

        self.go = False
        self.counter = 0

        # Name area
        self.name_lab = tk.Label(text="Full Name:", font=("Helvetica", 30), width=10)
        self.name_ent = tk.Entry(font=("Helvetica", 30), width=15)
        self.group_lab = tk.Label(text="Group:", font=("Helvetica", 30), width=10)
        self.group_ent = tk.Entry(font=("Helvetica", 30), width=15)
        self.name_but = tk.Button(text="Continue", command=self.login,
                                  font=("Helvetica", 30), width=10)

        self.group_lab.grid(column=0, row=1)
        self.group_ent.grid(column=1, row=1)
        self.name_lab.grid(column=0, row=0)
        self.name_ent.grid(column=1, row=0)
        self.name_but.grid(column=1, row=2)
        self.root.mainloop()

    def login(self):
        self.name = self.name_ent.get()
        self.group = self.group_ent.get()
        if self.name and (self.group == '1' or self.group == '2'):
            with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
                writer = csv.writer(f)
                row = ['Name', self.name]
                writer.writerow(row)
                row = ['Group', self.group]
                writer.writerow(row)
            self.name_lab.grid_forget()
            self.name_ent.grid_forget()
            self.name_but.grid_forget()
            self.root.quit()

login = App()

