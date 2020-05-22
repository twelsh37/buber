from tkinter import *
from PIL import ImageTk,Image


def donothing():
    filewin = Toplevel(buber)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def help_menu():
    filewin = Toplevel(buber)
    #button = Button(filewin, text="Tom woz 'ere")
    canvas = Canvas(buber, width=400, height=400)
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open("images/bluefootedboobie.png"))
    canvas.create_image(20, 20, anchor=NW, image=img)
    button.pack()

# Instansiate our window and set the size and title
buber = Tk()
buber.title("Buber")
buber.geometry("1024x768")

# Set our menu Itr=ems
menubar = Menu(buber)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=buber.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=help_menu)
menubar.add_cascade(label="Help", menu=helpmenu)

buber.config(menu=menubar)
buber.mainloop()
