#how to create simple GUI registration form.
#importing tkinter module for GUI application
from tkinter import *
import csv

#Creating object 'root' of Tk()
root = Tk()

#Providing Geometry to the form
root.geometry("550x250")

#Providing title to the form
root.title('Form')
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight-170, positionDown-60))

#this creates 'Label' widget for Registration Form and uses place() method.
label_0 =Label(root,text="Form", width=5,font=("bold",20))
label_0.place(x=0,y=0)

label_name =Label(root,text=" How do you feel right now ? Do not overthink one statement", width=50,font=("bold",10))
label_name.place(x=0,y=40)

label_ans =Label(root,text=" 1 --> Not at all   2--> somewhat  3 --> moderately so  4--> very much so", width=60,font=("bold",10))
label_ans.place(x=0,y=60)

label_1 =Label(root,text="I feel strained", width=20,font=("bold",10))
label_1.place(x=80,y=80)
var1=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var1, value=1).place(x=370,y=80)
Radiobutton(root,text="2",padx= 0, variable= var1, value=2).place(x=405,y=80)
Radiobutton(root,text="3",padx= 0, variable= var1, value=3).place(x=440,y=80)
Radiobutton(root,text="4",padx= 0, variable= var1, value=4).place(x=475,y=80)

label_2 =Label(root,text="I feel peaceful", width=20,font=("bold",10))
label_2.place(x=80,y=100)
var2=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var2, value=1).place(x=370,y=100)
Radiobutton(root,text="2",padx= 0, variable= var2, value=2).place(x=405,y=100)
Radiobutton(root,text="3",padx= 0, variable= var2, value=3).place(x=440,y=100)
Radiobutton(root,text="4",padx= 0, variable= var2, value=4).place(x=475,y=100)

label_3 =Label(root,text="I feel nervous", width=20,font=("bold",10))
label_3.place(x=80,y=120)
var3=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var3, value=1).place(x=370,y=120)
Radiobutton(root,text="2",padx= 0, variable= var3, value=2).place(x=405,y=120)
Radiobutton(root,text="3",padx= 0, variable= var3, value=3).place(x=440,y=120)
Radiobutton(root,text="4",padx= 0, variable= var3, value=4).place(x=475,y=120)

label_4 =Label(root,text="I feel comfortable", width=20,font=("bold",10))
label_4.place(x=80,y=140)
var4=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var4, value=1).place(x=370,y=140)
Radiobutton(root,text="2",padx= 0, variable= var4, value=2).place(x=405,y=140)
Radiobutton(root,text="3",padx= 0, variable= var4, value=3).place(x=440,y=140)
Radiobutton(root,text="4",padx= 0, variable= var4, value=4).place(x=475,y=140)

label_5 =Label(root,text="I feel indecisive", width=20,font=("bold",10))
label_5.place(x=80,y=160)
var5=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var5, value=1).place(x=370,y=160)
Radiobutton(root,text="2",padx= 0, variable= var5, value=2).place(x=405,y=160)
Radiobutton(root,text="3",padx= 0, variable= var5, value=3).place(x=440,y=160)
Radiobutton(root,text="4",padx= 0, variable= var5, value=4).place(x=475,y=160)

label_6 =Label(root,text="I feel content", width=20,font=("bold",10))
label_6.place(x=80,y=180)
var6=IntVar()
Radiobutton(root,text="1",padx= 0, variable= var6, value=1).place(x=370,y=180)
Radiobutton(root,text="2",padx= 0, variable= var6, value=2).place(x=405,y=180)
Radiobutton(root,text="3",padx= 0, variable= var6, value=3).place(x=440,y=180)
Radiobutton(root,text="4",padx= 0, variable= var6, value=4).place(x=475,y=180)

#this creates button for submitting the details provides by the user
Button(root, text='Submit' , width=20, command = root.destroy, bg="black",fg='white').place(x=210,y=210)


#this will run the mainloop.
root.mainloop()
results = ['Form2',var1.get(),var2.get(),var3.get(),var4.get(),var5.get(),var6.get()]
with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(results)
