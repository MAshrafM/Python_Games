from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand = 1)
        #quitButton = Button(self, text = "Quit", command = self.client_exit)
        #quitButton.place(x=0, y=0)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label = 'New File')
        file.add_command(label = 'Open')
        file.add_command(label = 'Save')
        file.add_separator()
        file.add_command(label = 'Close', command = self.client_close)
        file.add_command(label = 'Exit', command = self.client_exit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label = 'Undo')
        edit.add_command(label = 'Show Img', command=self.showImg)
        edit.add_command(label = 'Show TXT', command = self.showTXT)
        menu.add_cascade(label='Edit', menu = edit)

    def client_exit(self):
        quit()

    def client_close(self):
        exit()
    def showImg(self):
        load = Image.open("castle.png")
        render = ImageTk.PhotoImage(load)
        button = Button(self, image=render,text="click me", command=self.client_exit)
        button.image = render
        button.place(x=100,y=100)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def showTXT(self):
        text = Label(self, text="Hello, World")
        text.pack()

        
root = Tk()
root.geometry("400x400")
app = Window(root)
root.mainloop()
