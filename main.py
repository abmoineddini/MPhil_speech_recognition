from DataCollector import *
import matplotlib.pyplot as plt
import os
import pandas as pd
from os import listdir
from DataCollector import playAudioFile
import winsound
import random
#import time

dataCollection = True
CheckPort = input("Would you like to Start collecting Data : ")
Channel = input("Multichannel test or singleChannel test: (s for single m for multi)")
Method = input("Continious or Individual Collections? ")
if CheckPort == "y" or CheckPort == "Y" or CheckPort == "Yes" or CheckPort == "yes":
    COMPort = "COM4"     #input("Please Enter COM Port: ")
    print(COMPort)
    # CheckPort = input("Is that Correct?")

    while dataCollection:
        if Method == "c":
            AudioFiles = [f for f in listdir("AudioFiles/")]
            for i in AudioFiles:
                Name = i
                print(Name)
                print("here")
                Period = 10
                print("Startting to Collect Data for: ", Period, '(s)')
                # CheckPeriod = input("Is that Correct?")
                # if CheckPeriod == "n" or CheckPeriod == "N" or CheckPeriod == "no" or CheckPeriod == "No":
                #     Period = input("Please Enter the Desired Time Period: ")
                #     print(Period)
                #     print("Starting to Collect Data for: ", Period, '(s)')
                #     CheckName = input("Is that Correct?")

                AudioFileName = "AudioFiles/" + Name
                winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
                #playAudioFile(AudioFileName)
                CSVName = Name.replace('.wav', '')
                NameTest = True
                TrainingDataDirectory = [f for f in listdir("TrainingData")]
                testNum = 1
                while NameTest:
                    CSVNameCheck = CSVName + '-Test'+ str(testNum) + '.csv'
                    if CSVNameCheck in TrainingDataDirectory:
                        print("File Already exist, Trying another name.")
                        testNum = testNum+1
                    else:
                        CSVName = CSVName + '-Test'+ str(testNum)
                        NameTest = False
                print(CSVName)
                # [Channel1, Time] = collectData(COMPort, Period, CSVName)
                # plt.plot(Time, Channel1)
                # plt.show()
                # winsound.PlaySound(None, winsound.SND_PURGE)
                # DataCheck = input("Are you happy with the Data? ")
                # while DataCheck == "n" or DataCheck == "N" or DataCheck == "no" or DataCheck == "No":
                #     Nametoremove = "TrainingData/" + CSVName + ".csv"
                #     os.remove(Nametoremove)


                winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
                if Channel == "m":
                    [Channel1, Channel2, Channel3, Channel4, Time] = collectData_multiChannel(COMPort, Period, Name)
                    aaa = random.randint(0, 70)
                    if aaa == 25:
                        plt.plot(Time, Channel1)
                        plt.plot(Time, Channel2)
                        plt.plot(Time, Channel3)
                        plt.plot(Time, Channel4)
                        plt.show()
                elif Channel == "s":
                    [Channel1, Time] = collectData(COMPort, Period, CSVName)
                    aaa = random.randint(0, 70)
                    if aaa == 25:
                        plt.plot(Time, Channel1)
                        plt.show()
                winsound.PlaySound(None, winsound.SND_PURGE)
                # DataCheck = input("Are you happy with the Data? ")

        else:
            AudioFiles = [f for f in listdir("AudioOriginal")]
            for i in AudioFiles:
                Name = i
                print(Name)
                print("here")

                AudioFileName = "AudioOriginal/" + Name
                # playAudioFile(AudioFileName)
                CSVName = Name.replace('.wav', '')
                NameTest = True
                TrainingDataDirectory = [f for f in listdir("TrainingData")]
                testNum = 1

                while NameTest:
                    CSVNameCheck = CSVName + '-Test'+ str(testNum) + '.csv'
                    if CSVNameCheck in TrainingDataDirectory:
                        print("File Already exist, Trying another name.")
                        testNum = testNum+1
                    else:
                        CSVName = CSVName + '-Test'+ str(testNum)
                        NameTest = False
                print(CSVName)
                #winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
                # [Channel1, Time] = collectDataMet2(COMPort, CSVName, AudioFileName)
                # plt.plot(Time, Channel1)
                # plt.show()
                # winsound.PlaySound(None, winsound.SND_PURGE)
                # #DataCheck = input("Are you happy with the Data? ")
                # DataCheck = 'y'
                # while DataCheck == "n" or DataCheck == "N" or DataCheck == "no" or DataCheck == "No":
                #     Nametoremove = "TrainingData/" + CSVName + ".csv"
                #     os.remove(Nametoremove)

                    # winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
                if Channel == "m":
                    print("multiChannel Channel individual data set")
                    time.sleep(5)
                    [Channel1, Channel2, Channel3, Channel4, Time] = collectDataMet2_multiChannel(COMPort, CSVName, AudioFileName)
                    aaa = random.randint(0, 2)
                    if aaa == 2:
                        plt.plot(Time, Channel1)
                        plt.show()
                        plt.plot(Time, Channel2)
                        plt.show()
                        plt.plot(Time, Channel3)
                        plt.show()
                        plt.plot(Time, Channel4)
                        plt.show()


                #elif Channel == "i":
                else:
                    # print("Single Channel individual data set")
                    # time.sleep(5)
                    [Channel1, Time] = collectDataMet2(COMPort, CSVName, AudioFileName)
                    aaa = random.randint(0, 70)
                    aaa = 2
                    if aaa == 2:
                        plt.plot(Time, Channel1)
                        plt.show()

                winsound.PlaySound(None, winsound.SND_PURGE)

        #ToContinue = input("would you like to Continue with collecting data? ")
        ToContinue = 'y'
        if ToContinue == "n" or ToContinue == "N" or ToContinue == "No" or ToContinue == "no":
            dataCollection = False



StartPreprocessing = input("Should I Start the Preprocessing? ")
if StartPreprocessing == "y" or StartPreprocessing == "Y" or StartPreprocessing == "Yes" or StartPreprocessing == "yes":

    import glob

    if os.path.isdir("Figure/Training"):
        print("Adding to Figure Directory")
    else:
        os.mkdir("Figure/Training")
        os.mkdir("Figure/Testing")

    csv_files = glob.glob(os.path.join("TrainingData/", "*.csv"))

    from PreprocessorSpeechrecognition import figure_maker, Classifier, PreprocessingMeth2
    from csv import writer



    for x in csv_files[0:]:
        dataFileName = x
        print(x)
        NAMEunprocessed = x.replace(".csv", "")
        NAMEunprocessed = NAMEunprocessed.split("\\")
        NAMEunprocessed = NAMEunprocessed[1]
        NAMEunprocessed = NAMEunprocessed.split("-")
        x = NAMEunprocessed[0]
        x = x[2:len(x)]
        check = 0


        if os.path.isfile("ProcessedData.csv"):
            print("Processed data collector Already exists")

            PDCL = pd.read_csv("ProcessedData.csv")
            print(PDCL)
            ProcessedDataChecklist = PDCL.to_numpy()
            ProcessedDataChecklist = ProcessedDataChecklist[:]

            if dataFileName in ProcessedDataChecklist:
                check = 1
                continue

        if check == 0:
            [FolderSTFTTraining, FolderSTFTTesting] = Classifier(x)

            df = pd.read_csv(dataFileName)
            data = df.to_numpy()
            print(dataFileName)

            if len(data)>40000:
                figure_maker(data, FolderSTFTTraining, FolderSTFTTesting, dataFileName)
            else:
                PreprocessingMeth2(data, FolderSTFTTraining, FolderSTFTTesting, dataFileName)

            if os.path.isfile("ProcessedData.csv"):
                with open("ProcessedData.csv", 'a+' ,newline='') as f_object:
                    # Pass the CSV  file object to the writer() function
                    writer_object = writer(f_object)
                    # Result - a writer object
                    # Pass the data in the list as an argument into the writerow() function
                    writer_object.writerow([dataFileName])
                    # Close the file object
                    f_object.close()
            else:
                dict = {"File Name": [dataFileName]}
                df = pd.DataFrame(dict)
                df.to_csv("ProcessedData.csv")

        #CheckPoint = input("Would you like to continue? ")
        #plt.close('all')



print("Finished Creating Relevant Files")


StartTraining = input("Should I Start the Training? ")
while StartTraining == "n" or StartTraining == "N" or StartTraining == "no" or StartTraining == "No":
    StartTraining = input("Should I Start the Training? ")


trainingSTFT = "Figure/Training"
testingSTFT = "Figure/Testing"

from MachineLearning import *
img_size = 64
# STFT Training
[STFTModel, acc, val_acc, loss, val_loss]= CNN_Training(trainingSTFT, testingSTFT, 150, LearningRate=0.0001, dataType="STFT", img_size=img_size)

STFTModel.save("VoiceRecCNN")

from csv import writer
for i in range(len(acc)):
    FileAdd = [acc[i], val_acc[i], loss[i], val_loss[i]]
    with open("AccuracyHistory.csv", 'a+', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(FileAdd)
        # Close the file object
        f_object.close()
        FileAdd = []


# Testinig Peformance
print("STFT CNN Test result")
[y_val, predictions] = TestingNetwrok(STFTModel, testingSTFT, img_size)

for i in range(len(y_val)):
    FileAdd = [y_val[i], predictions[i]]
    with open("TestingValidationCNN.csv", 'a+', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(FileAdd)
        # Close the file object
        f_object.close()
        FileAdd = []



STFTmodelName = 'STFTModel.yaml'

Save_CNN(STFTModel, Name=STFTmodelName)

# import cv2
#
# img_size = 300
# def Preprocess(path):
#     img_arr = cv2.imread(path)
#     img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
#     resized_arr = cv2.resize(img_arr, (img_size, img_size))
#     norm_arr = np.array(resized_arr) / 255
#     return norm_arr.reshape(-1, img_size, img_size, 1)
#
# sample = Preprocess("TestingFigure.png")
#
# predict = STFTModel.predict([Preprocess("TestingFigure.png")])
# print(predict)