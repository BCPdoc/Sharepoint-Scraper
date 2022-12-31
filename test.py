from tkinter import *

root = Tk()

def change(frame):
    frame.tkraise() # Raising the passed frame

window1 = Frame(root)
window2 = Frame(root)

window1.grid(row=0,column=0) # Grid in the same location so one will cover/hide the other
window2.grid(row=0,column=0)

# Contents inside your frame...
Label(window1,text='This is page 1',font=(0,21)).pack()
Label(window2,text='This is page 2',font=(0,21)).pack()

# Buttons to switch between frame by passing the frame as an argument
Button(root,text='Page 1',command=lambda: change(window1)).grid(row=1,column=0,stick='w')
Button(root,text='Page 2',command=lambda: change(window2)).grid(row=1,column=0,stick='e')

root.mainloop()