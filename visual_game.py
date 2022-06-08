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

        self.vis_mem = MemoryV(self)
        self.title_l = tk.Label(font=("Helvetica", 50), width=22)

        self.name_lab = tk.Label(text="GAME 3 : Visual memory", font=("Helvetica", 40))
        self.name_rules = tk.Label(text="Rules :\n Turquoise tiles are displayed for a few seconds,\n when the turquoise color disappears,\n click only on those tiles", font=("Helvetica", 25))
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
        self.vis_mem.draw()


class MemoryV:
    def __init__(self, app):
        self.app = app

        self.score1 = 'N/A'
        self.fails = 0
        self.grid = dict()
        self.lit = []
        self.picked = []

        self.level = 1

        self.title_lab = tk.Label(text="Visual Game", font=("Helvetica", 40))

        self.go_but = tk.Button(text="Go?", bg="seagreen1", font=("Helvetica", 20), command=self.go, width=20)
        self.frame = tk.Frame(bg="deepskyblue2")

    def draw(self):
        self.app.root.title("Visual Memory")

        self.go_but.grid(row=1, column=1)

        self.title_lab.grid(row=1, column=1)
        self.go_but.grid(row=2, column=0, columnspan=4)

    def undraw(self):
        self.go_but.grid_forget()
        self.frame.grid_forget()
        for i in self.grid.copy():
            for b in self.grid[i].buttons.values():
                b.destroy()
            del self.grid[i]
        self.title_lab.grid_forget()

    def go(self):
        self.go_but.grid_forget()
        self.level = 1

        self.grid = dict()

        self.frame.grid(column=0, row=2, columnspan=20)
        for i in range(1, self.level+3):
            self.grid[i] = Row(self.frame, self.app, i, self.level + 2)
            self.grid[i].draw()
        self.pick_squares()

    def pick_squares(self):
        self.lit = []
        self.picked = []
        for r in self.grid.values():
            for b in r.buttons.values():
                b.configure(state='disabled', bg="blue2")
        n = random.randint(self.level+1, self.level+2)
        i = 1
        while i <= n:
            x = random.randint(1, self.level+2)
            y = random.randint(1, self.level+2)
            if [x, y] not in self.lit:
                self.lit.append([x, y])
                self.grid[y].buttons[x].configure(bg="turquoise")
                i += 1
        self.app.root.after(1000+(self.level*1500), self.clear_squares)

    def clear_squares(self):
        for r in self.grid.values():
            for b in r.buttons.values():
                b.configure(bg="royal blue", state='normal')

    def check(self):
        if sorted(self.lit) == sorted(self.picked):
            self.level += 1
            for r in self.grid.values():
                r.add()
            self.grid[len(self.grid)+1] = Row(self.frame, self.app, len(self.grid)+1, self.level + 2)
            self.grid[len(self.grid)].draw()

            for r in self.grid.values():
                for b in r.buttons.values():
                    b.configure(state='disabled')

            self.app.root.after(1000, self.pick_squares())

    def back(self):
        self.do_checks()
        self.undraw()
        self.app.draw()

    def do_checks(self):
        self.fails +=1
        # if self.fails == 1:
        #     self.score1 = self.level-1
        if self.fails == 1:
            with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
                writer = csv.writer(f)
                row = ['Visual', str(self.level-1)]
                writer.writerow(row)
            self.app.root.quit()

        self.app.root.after(400, self.undraw())
        self.app.root.after(401, self.draw())

class Row:
    def __init__(self, root, app, row, width):
        self.root = root
        self.app = app
        self.row = row
        self.width = width

        self.buttons = dict()
        for i in range(1, width+1):
            self.buttons[i] = tk.Button(self.root, width=8, height=4, bg="blue2",
                                        state='disabled', command=lambda x=i: self.click(x))

    def draw(self):
        for i in self.buttons:
            self.buttons[i].grid(row=self.row, column=i)

    def add(self):
        l = len(self.buttons)
        self.buttons[l+1] = tk.Button(self.root, width=8, height=4, bg="blue2", state='disabled',
                                                      command=lambda: self.click(l+1))
        self.buttons[l+1].grid(row=self.row, column=l+1)

    def click(self, col):
        if [col, self.row] in self.app.vis_mem.lit:
            self.buttons[col].configure(bg="turquoise2", state='disabled')
            self.app.vis_mem.picked.append([col, self.row])
            self.app.vis_mem.check()
        else:
            self.buttons[col].configure(bg="violet red")
            for r in self.app.vis_mem.grid:
                for b in self.app.vis_mem.grid[r].buttons:
                    self.app.vis_mem.grid[r].buttons[b].configure(state='disabled')
                    if [b, r] in self.app.vis_mem.lit:
                        self.app.vis_mem.grid[r].buttons[b].configure(bg='turquoise2')
            self.app.root.after(1500, self.app.vis_mem.do_checks)



game = App()