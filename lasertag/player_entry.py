import os
import time
from tkinter import * 

player_entry = Tk(className='Player Entry')
height = 720
width = 1280

#geometry creates a new window using the given h,w,x,y values
x = (player_entry.winfo_screenwidth()//2)-(width//2)
y = (player_entry.winfo_screenheight()//2)-(height//2)
player_entry.geometry('{}x{}+{}+{}'.format(width,height,x,y))
player_entry.resizable(False,False)

giant_label = Label(player_entry, text="Finish Later", font=("Helvetica", 72))
giant_label.place(relx=0.5, rely=0.5, anchor=CENTER)

player_entry.mainloop()