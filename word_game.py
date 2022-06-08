from tkinter import messagebox
import tkinter as tk
import random
import csv

from tkinter import messagebox
import tkinter as tk
import random
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

        self.high_scores_n = list()

        self.word_mem = MemoryW(self)
        self.title_l = tk.Label(font=("Helvetica", 50), width=22)

        self.name_lab = tk.Label(text="GAME 2 : Words memory", font=("Helvetica", 40))
        self.name_rules = tk.Label(text="Rules : \n Words are displayed, click on 'new'\n if they were not displayed before, \n else, click on 'seen'", font=("Helvetica", 25))
        self.name_but = tk.Button(text="Click here to play", command=self.login,
                                  font=("Helvetica", 25),bg="green", width=15)

        self.name_lab.grid(column=0, row=0)
        self.name_rules.grid(column=0, row=1)
        self.name_but.grid(column=0, row=2)

        self.root.mainloop()

    def login(self):
        self.name_lab.grid_forget()
        self.name_but.grid_forget()
        self.name_rules.grid_forget()
        self.word_mem.draw()



class MemoryW:
    def __init__(self, app):
        self.app = app
        self.fails = 0
        self.seen1 = 'N/A'

        with open("/home/tanguy/catkin_ws/src/state_machine/scripts/FREQ.TXT", 'r') as f:
            self.all_words = [x.strip('\n') for x in f.readlines()]

        self.max = 10
        self.word = ''

        self.seen_l = []
        self.condensed = []

        self.title_lab = tk.Label(text="Word Game", font=("Helvetica", 40))

        self.go_but = tk.Button(text="Go?", bg="seagreen1", font=("Helvetica", 40), command=self.go, width=20)

        self.word_lab = tk.Label(text="", font=("Helvetica", 40), width=10)

        self.new_but = tk.Button(text="New", font=("Helvetica", 40),  command=self.new, width=10, bg = 'green')
        self.seen_but = tk.Button(text="Seen", font=("Helvetica", 40),  command=self.seen, width=10, bg = 'red')

    def go(self):
        self.go_but.grid_forget()
        self.word_lab.grid(row=2, column=1, columnspan=2)
        self.new_but.grid(row=2, column=0)
        self.seen_but.grid(row=2, column=3)

        random.shuffle(self.all_words)
        self.condensed = self.all_words[:self.max]
        self.max = 20
        self.word = ''
        self.seen_l = []

        self.pick_new()

    def new(self):
        if self.word not in self.seen_l:
            self.seen_l.append(self.word)
            self.new_but.configure(disabledforeground='green', state='disabled')
            self.seen_but.configure(disabledforeground='red', state='disabled')
            self.app.root.after(1000, self.pick_new)
        else:
            self.new_but.configure(disabledforeground='red', state='disabled')
            self.seen_but.configure(disabledforeground='green', state='disabled')
            self.app.root.after(1500, self.do_checks)

    def seen(self):
        if self.word in self.seen_l:
            self.new_but.configure(disabledforeground='red', state='disabled')
            self.seen_but.configure(disabledforeground='green', state='disabled')
            self.app.root.after(1000, self.pick_new)
        else:
            self.new_but.configure(disabledforeground='green', state='disabled')
            self.seen_but.configure(disabledforeground='red', state='disabled')
            self.app.root.after(1500, self.do_checks)

    def do_checks(self):
        self.fails += 1
        # if self.fails == 1:
        #     self.seen1 = len(self.seen_l)
        if self.fails == 1:
            with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
                writer = csv.writer(f)
                row = ['Word', str(len(self.seen_l))]
                writer.writerow(row)
            self.app.root.quit()

        self.app.root.after(400, self.undraw())
        self.app.root.after(401, self.draw())

    def pick_new(self):
        if len(self.seen_l) >= (len(self.condensed) / 3) * 2:
            self.max += 7
            self.condensed = self.all_words[:self.max]
        self.word = random.choice(self.condensed)
        self.word_lab.configure(text=self.word)
        self.new_but.configure(state='normal')
        self.seen_but.configure(state='normal')

    def draw(self):
        self.app.root.title("Word Memory")

        self.max = 20
        self.word = ''
        self.seen_l = []

        self.go_but.grid(row=1, column=1)

        self.title_lab.grid(row=1, column=1)
        self.go_but.grid(row=2, column=0, columnspan=4)

    def undraw(self):
        self.go_but.grid_forget()

        self.title_lab.grid_forget()
        self.word_lab.grid_forget()
        self.new_but.grid_forget()
        self.seen_but.grid_forget()

    def back(self):
        self.undraw()
        self.app.draw()

game = App()