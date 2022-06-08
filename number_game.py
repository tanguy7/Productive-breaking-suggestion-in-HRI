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
        self.root.geometry("+{}+{}".format(positionRight-170, positionDown-60))
        self.root.title("Menu")
        self.name = ''

        self.go = False
        self.counter = 0

        self.high_scores_n = list()

        self.num_mem = MemoryN(self)
        self.title_l = tk.Label(font=("Helvetica", 50), width=22)

        self.name_lab = tk.Label(text="GAME 1 : Number memory", font=("Helvetica", 40))
        self.name_rules = tk.Label(text="Rules : \n Recall the number displayed, \n than type it and click 'check'", font=("Helvetica", 25))
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
        self.num_mem.draw()




class MemoryN:
    def __init__(self, app):

        self.app = app
        self.fails = 0
        self.state = 0
        self.go = False
        self.digits = 0
        self.timer = 0
        self.current_num = 0
        self.score1 = 'N/A'
        
        self.title_lab = tk.Label(text="Number Game", font=("Helvetica", 40), width = 17)
        self.num_lab = tk.Label(font=("Helvetica", 35))
        
        self.text = tk.Text(width=15, height=1, font=("Helvetica", 40))
        self.text.focus_set()
        self.text.mark_set("insert", "%d.%d" % (1,1))
        self.submit = tk.Button(text="Check", font=("Helvetica", 35),  command=self.click, width=10)       
        self.bar = tk.Label(bg="light sky blue")
        
    def draw(self):
        self.app.root.title("Number Memory")
        self.go = True
        
        self.digits = 5
        self.timer = round(self.digits * 1.4)

        self.state = 0
        
        self.current_num = random.randint(10 ** (self.digits-1) - 1, (10 ** self.digits) - 1)

        self.num_lab.configure(text=self.current_num)
        self.bar.configure(width=min(50,self.timer*5+1))
        self.title_lab.grid(row=1, column=1)
        self.num_lab.grid(row=2, column=0, columnspan=4)
        self.bar.grid(row=3, column=0, columnspan=4)

        self.update()        

    def undraw(self):
        self.go = False
        self.title_lab.grid_forget()
        self.num_lab.grid_forget()
        self.text.grid_forget()
        self.bar.grid_forget()
        self.submit.grid_forget()

    def back(self):
        self.undraw()
        self.app.draw()

    def update(self):
        if self.go:
            if self.state == 0 and self.timer > 0:
                self.timer -= 1
                self.bar.configure(width=min(25,self.timer*5+1))
            elif self.timer == 0 and self.state == 0:
                self.bar.configure(bg=self.app.root.cget("bg"))
                self.state = 1
            elif self.state == 1:
                self.text.configure(state='normal', fg="black")
                self.text.delete("1.0", "end")
                self.num_lab.grid_forget()
                self.bar.grid_forget()
                self.text.grid(row=2, column=0, columnspan=4)
                self.submit.grid(row=3, column=0, columnspan=4)
                self.submit.configure(state='normal')

                self.state = 2
            self.app.root.after(1000, self.update)

    def fails(self):
        return self.fails
        
    def click(self):
        guess = self.text.get("1.0", "end").strip('\n')
        if guess == str(self.current_num):
            self.text.configure(fg="green", state='disabled')
            self.submit.configure(disabledforeground="green", state='disabled')
            self.digits += 1
            self.app.root.after(1000, self.new)
        else:
            self.fails += 1
            if self.fails == 1:
                with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
                    writer = csv.writer(f)
                    row = ['Number', str(self.digits-1)]
                    writer.writerow(row)
                self.app.root.quit()

    def new(self):
        if self.go:
            self.current_num = random.randint(10 ** (self.digits-1), (10 ** self.digits) - 1)
            self.timer = round(self.digits * 1.4)
            self.state = 0
            self.text.grid_forget()
            self.submit.grid_forget()

            self.num_lab.configure(text=self.current_num)
            self.bar.configure(width=self.timer*2)

            self.num_lab.grid(row=2, column=0, columnspan=4)
            self.bar.grid(row=3, column=0, columnspan=4)
            self.bar.configure(bg="light sky blue")

game = App()




