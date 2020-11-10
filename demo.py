import tkinter as tk
import numpy as np
from tkinter import filedialog, Menu
import cv2

main = tk.Tk();
main.title("Demo Valley-Emphasis")

def selectImg():
    imgFile = filedialog.askopenfilename(initialdir = 'C:\\Users\\ACER\\Desktop\\xla', title="Chon anh",
       filetypes = (("jpeg files, png files","*.jpg, *.png"),("all files","*.*"))
    )
    displayImg(imgFile)


def displayImg(src):
    img = cv2.imread(src)
    img = cv2.resize(img,(800,500))
    cv2.imshow("Anh goc", img)
    
    global image 
    image = img

    
arrayVariance = []
def valleyEmphasis():
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([img_gray], [0], None, [255], [0,255]);
    cv2.imshow("anh xam", img_gray)

    height = image.shape[0]
    width = image.shape[1]
    sumPixels = height * width; 

    for i in range(len(histogram)):
        bg,fg = np.split(histogram, [i])

        weightB = np.sum(bg)/sumPixels
        weightF = np.sum(fg)/sumPixels

        meanB = np.sum([i*p for i,p in enumerate(bg)])/np.sum(bg)
        meanF = np.sum([i*p for i,p in enumerate(fg)])/np.sum(fg)
        meanB, meanF = np.nan_to_num(meanB),np.nan_to_num(meanF)

        varianceB = np.sum([(j-meanB)**2*t for j,t in enumerate(bg)])/np.sum(bg) 
        varianceF = np.sum([(j-meanF)**2*t for j,t in enumerate(fg)])/np.sum(fg) 
        varianceB, varianceF = np.nan_to_num(varianceB),np.nan_to_num(varianceF)

        varainceT = varianceB/sumPixels
        arrayVariance.append((1-varainceT)*weightB*varianceB + weightF*varianceF);


    varianceMin = np.argmin(arrayVariance)
    print(varianceMin)
    label = tk.Label(text="T=" + str(varianceMin))
    label.grid(row = 2, column = 0, pady = 1, padx = 2) 
    (thresh, finalImage) = cv2.threshold(img_gray,varianceMin,255,cv2.THRESH_BINARY)
    cv2.imshow("valley", finalImage)

def menuBar():
    #menubar = Menu(main)  
    #menubar.add_command(label="Open Image", command=selectImg )  
    #menubar.add_command(label="Valley-Emphasis", command=valleyEmphasis )  
    #main.config(menu=menubar)  

    btnOpen = tk.Button(text="Open Image", width=10, height=4, bg="#5882FA", fg="white", command=selectImg)
    btnHandle = tk.Button(text="Valley-Emphasis", width=20, height=4, bg="#FF8000", command=valleyEmphasis)
    btnOpen.grid(row = 1, column = 0, pady = 1) 
    btnHandle.grid(row = 1, column = 1, pady = 1) 
      

menuBar()

main.mainloop()





