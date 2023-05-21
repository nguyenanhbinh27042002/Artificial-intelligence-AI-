from email.mime import message
import cv2 as cv
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from matplotlib.pyplot import show
import numpy as np
from tkinter import messagebox
from tensorflow import keras,expand_dims
from keras.utils import load_img
from keras.utils.image_utils import img_to_array
from tkinter import filedialog

from Frames import *
from PredictVirus import *
from displayCovid import *

def run():
    global anhbia
    anhbia.destroy()
anhbia = tkinter.Tk()
anhbia.geometry("1200x720")
# ten cua so cua anh bia
anhbia.title("The Virus Detection")
# mo hinh anh bia
anh=Image.open("BIA.png")
# chinh kich thuoc anh bia
resizeimage=anh.resize((1200, 720))
a = ImageTk.PhotoImage(resizeimage)
img=tkinter.Label(image=a)
img.grid(column=0,row=0)
Btn=tkinter.Button(anhbia,text="RUN",font=("Times New Romen",20),command= run )
Btn.place(x=800, y=600)
anhbia.mainloop()

class Gui:
    # Thiết lập ban đầu
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        # Gobal(toàn cục)
        global MainWindow
        # Tạo một cửa sổ bằng lệnh TK()
        MainWindow = tkinter.Tk()
        # kích thước
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayVirus()
        self.fileName = tkinter.StringVar()
        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        # thêm fisrtFrame vào listOfWinFrame
        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="The SARS and Covid Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))
        # mo hinh anh bia

        anh = Image.open("anhbia.jpg")
        # chinh kich thuoc anh lena
        resizeimage = anh.resize((500, 350))
        a = ImageTk.PhotoImage(resizeimage)
        img = tkinter.Label(image=a)
        img.place(x=50, y=320)

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Virus SARS and Covid", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View The Lung Infected Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictVirus(mriImage)
            print(res)

            if res[0][0] > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Phat Hien Covid", height=1, width=50)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Khong Phat Hien Covid", height=1, width=50)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=500, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayVirus, self.DT)

            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if (len(self.listOfWinFrame) > 1):
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")
mainObj = Gui()
