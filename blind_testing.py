import serial
import numpy as np
import time

from PreprocessorSpeechrecognition import *
import cv2
import tensorflow as tf
from tkinter import *

ws = Tk()
ws.title('Voice Recognition')
ws.geometry('800x600')
ws.config(bg='#000000')

mylabel = Label(ws,
                text="...",
                bg='#000000',
                fg='#ffffff',
                font='Times 32',
                width=50,
                height=10)

mylabel.pack()
ws.update()

#COMPort = input("Please enter the COM port: ")
COMPort = 'COM6'
arduino = serial.Serial(COMPort, 2000000, timeout=1)
model = tf.keras.models.load_model("VoiceRecCNN")

Voltage = []
Time = []
dataCollection = False
dataAvailability = False
i = 0
j = 0
arr1 = []
arr2 = []
arr3 = []
arr4 = []
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
FirstCounter = True
while True:
    line = arduino.readline()
    if line != (''):
        #print(line)
        try:
            string = line.decode()
        except:
            print("ignored")
        else:
            numS = string.replace("\r\n", '')

            if numS.isdigit():
                print(int(numS))
                if int(numS) < 210:
                    dataCollection=False
                    if counter1<250:
                        counter1 +=1
                        arr1.append(int(numS))
                    elif counter1>=250 and counter1<500:
                        counter1 +=1
                        counter2 +=1
                        arr1.append(int(numS))
                        arr2.append(int(numS))
                    elif counter1>=500 and counter1<750:
                        counter1 +=1
                        counter2 +=1
                        counter3 +=1
                        arr1.append(int(numS))
                        arr2.append(int(numS))
                        arr3.append(int(numS))
                    else:
                        counter1 +=1
                        counter2 +=1
                        counter3 +=1
                        counter4 +=1
                        arr1.append(int(numS))
                        arr4.append(int(numS))
                        arr2.append(int(numS))
                        arr3.append(int(numS))


                    if counter4 == 250 and counter1 > 250:
                        counter1 = 0
                        arr1 = []

                    elif counter1==250 and counter2 > 250:
                        counter2 = 0
                        arr2 = []

                    elif counter2==250 and counter3 > 250:
                        counter3 = 0
                        arr3 = []

                    elif counter3==250 and counter4 > 250:
                        counter4 = 0
                        arr4 = []

                else:
                    dataCollection = True
                    Voltage.append(int(numS))
                    Time.append(i / 4000)
                    i = i + 1
                    j = 8000
                    print("StartingDataCollection")


    while dataCollection:
        line = arduino.readline()
        print(line)
        if line != (''):
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    if int(numS)<210:
                        j = j-1
                    else:
                        j = 8000

                    Voltage.append(int(numS))
                    Time.append(i / 4000)
                    i = i+1

                    if j<1:
                        dataCollection=False
                        dataAvailability = True

    if dataAvailability:
        SIZESLIST = [len(arr1), len(arr2), len(arr3), len(arr4)]
        maxval = max(SIZESLIST)
        maxlen = SIZESLIST.index(maxval)
        V = []
        t = []
        if FirstCounter:
            predictVal = 6
            FirstCounter = False
            dataAvailability = False

        else:
            if maxlen == 0:
                V = np.vstack([arr1, Voltage])
                tAdj = np.linspace(0, (len(arr1)-1)*0.00025, len(arr1))
                tAdjm = tAdj[len(tAdj)-1]+0.00025
                for i in range(len(Time)):
                    Time[i] = Time[i]+tAdjm
                t = np.vstack([tAdj, Time])

            elif maxlen == 1:
                V = np.vstack([arr2, Voltage])
                tAdj = np.linspace(0, (len(arr2)-1)*0.00025, len(arr2))
                tAdjm = tAdj[len(tAdj)-1]+0.00025
                for i in range(len(Time)):
                    Time[i] = Time[i]+tAdjm
                t = np.vstack([tAdj, Time])
            elif maxlen == 2:
                V = np.vstack([arr3, Voltage])
                tAdj = np.linspace(0, (len(arr3) - 1) * 0.00025, len(arr3))
                tAdjm = tAdj[len(tAdj) - 1] + 0.00025
                for i in range(len(Time)):
                    Time[i] = Time[i] + tAdjm
                t = np.vstack([tAdj, Time])
            else:
                V = np.vstack([arr4, Voltage])
                tAdj = np.linspace(0, (len(arr4)-1)*0.00025, len(arr4))
                tAdjm = tAdj[len(tAdj)-1]+0.00025
                for i in range(len(Time)):
                    Time[i] = Time[i]+tAdjm
                t = np.vstack([tAdj, Time])

            plt.plot(t, V)
            plt.show()

            TestingPreprocessing(V, t)
            img_size = 300
            V = []
            t = []
            Voltage = []
            Time = []
            i = 0
            j = 0
            dataAvailability = False
            def Preprocess(path):
                img_arr = cv2.imread(path)[..., ::-1]
                resized_arr = cv2.resize(img_arr, (img_size, img_size))
                norm_arr = np.array(resized_arr) / 255
                return norm_arr.reshape(-1, img_size, img_size, 3)


            predict = model.predict([Preprocess("TestingFigure.png")])
            print(predict)

            predictVal = np.argmax(predict)

        if  predictVal == 0:
            text = 'or To take Arms\nagainst a sea of\ntroubles and\n by opposing end them'
        elif predictVal == 1:
            text = 'that is the question'
        elif predictVal == 2:
            text = 'to be or not to be'
        elif predictVal == 3:
            text = 'to die'
        elif predictVal == 4:
            text = 'to sleep no more'
        elif predictVal == 5:
            text = 'whether this nobler\n in the mind to suffer\n the slings and arrows of\n outrageous fortune'
        else:
            text = '...'
        mylabel.config(text=text)
        mylabel.pack()
        ws.update()
        time.sleep(5)
        mylabel.config(text='...')
        mylabel.pack()
        ws.update()
