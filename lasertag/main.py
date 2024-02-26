# tkinter is used to create a window//box for displaying things
# PIL was needed to implement the image into the window
import os
import time

from tkinter import * 
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
import udp_sockets
import threading

#create sockets
udp_sockets.create_sockets()

#create thread for receiving statuses
socket_thread = threading.Thread(target=udp_sockets.receive_data)
socket_thread.start()

# creating an instance of a TK object named splash for the first display case
splash = Tk(className='Loading')

#image_logo -> open the image then resize it using the given resolution of the window
image_logo = Image.open("images//logo.jpg")
height = 720
width = 1280
image_logo = image_logo.resize((width,height),Image.LANCZOS)
image_logo = ImageTk.PhotoImage(image_logo)
#geometry creates a new window using the given h,w,x,y values
x = (splash.winfo_screenwidth()//2)-(width//2)
y = (splash.winfo_screenheight()//2)-(height//2)
splash.geometry('{}x{}+{}+{}'.format(width,height,x,y))
splash.resizable(False,False)
logo = Label(image = image_logo)
logo.pack(fill=BOTH,expand=YES)

def fillbar(currentprog=0):
    i = 100/3
    if currentprog <= 100:
        progbar['value'] = currentprog
        currentprog += i
        splash.after(1000,fillbar,currentprog)
    else:
        splash.withdraw()
        os.system("python3 player_entry.py")
        splash.destroy()
        udp_sockets.game_start()



prog = Label(splash, text="Loading...", font = ('Arial',13,'bold'),fg = '#14183e',bg = '#71b3ef')
prog.place(x=100,y=670)
progbar = Progressbar(splash,orient=HORIZONTAL,length=1080,mode='determinate')
progbar.place(x=100,y=700)

fillbar()


splash.mainloop()