import tkinter as tk
import numpy as np
from tkinter import filedialog, Menu
import cv2
from matplotlib import pyplot as plt

main = tk.Tk();
main.title("Demo Valley-Emphasis")
main.geometry('300x250')

def selectImg():
    imgFile = filedialog.askopenfilename(initialdir = 'C:\\Users\\ACER\\Desktop\\xla\\images', title="Chọn ảnh",
       filetypes = (("jpeg files, png files","*.jpg, *.png"),("all files","*.*"))
    )
    displayImg(imgFile)


def displayImg(src):
    img = cv2.imread(src)
    img = cv2.resize(img,(800,500))
    cv2.imshow("Anh goc", img)
    
    global image 
    image = img


def valleyEmphasis():
    valley = []

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([img_gray], [0], None, [255], [0,255]);

    plt.plot(histogram)

    height = image.shape[0]
    width = image.shape[1]
    totalPixel = height * width; 

    for i in range(len(histogram)):
        bg,fg = np.split(histogram, [i])

        weight1 = np.sum(bg)/totalPixel 
        weight2 = np.sum(fg)/totalPixel 

        mean1 = np.sum([i*p for i,p in enumerate(bg)])/weight1
        mean2 = np.sum([i*p for i,p in enumerate(fg)])/weight2
        mean1, mean2 = np.nan_to_num(mean1), np.nan_to_num(mean2)


        #--------------------------------------------
        pT = histogram[i]/totalPixel 
        #--------------------------------------------
        #valley.append((1-pT)*(weight1*weight2*(mean1-mean2)**2));
        valley.append((1-pT)*(weight1*weight2*(mean1-mean2)**2));
        


    valleyThresh = np.argmax(valley)

    (thresh, valleyImage) = cv2.threshold(img_gray,valleyThresh,255,cv2.THRESH_BINARY)
    cv2.imshow("Valley T= " + str(valleyThresh), valleyImage)
    plt.show()
    cv2.waitKey()
    cv2.destroyAllWindows()

def menuBar():
    title = tk.Label(text="Valley-emphasis", font=15, pady=10)
    title.pack()

    btnOpen = tk.Button(text="Open Image", width=15, height=3, bg="#809fff",command=selectImg)
    btnHandle = tk.Button(text="Valley-emphasis", width=15, height=3, bg='#ff9933', command=valleyEmphasis)
    btnOpen.pack(padx=10, pady=10)
    btnHandle.pack(padx=10, pady=10)
  
menuBar()
main.resizable(True, True)
main.mainloop()




