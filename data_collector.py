import serial
import winsound

def playAudioFile(Name):
    # AudioFileName = Name.split('/')
    # AudioFileName = AudioFileName[1].split('.')
    # AudioFileName = "AudioOriginal/"+AudioFileName[0]+'.wav'
    winsound.PlaySound(Name, winsound.SND_ASYNC | winsound.SND_ALIAS )


def collectData(COMPort, Period, Name):
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    Channel1 = []
    # Channel2 = []
    # Channel3 = []
    # Channel4 = []
    Time = []
    #def animate(xVal, yVal):
    period = int(Period)
    period = int(period*4000/3.5)
    for i in range(period):
        line = arduino.readline()

        if line != (''):
            print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                # vals = numS.split(" ")
                if numS.split(" ")[0].isdigit():
                #if vals[0].isdigit():
                    # if vals[1].isdigit():
                    #     if vals[2].isdigit():
                    #         if vals[3].isdigit():
                    #vals = numS.split(" ")
                    #Val1 = int(numS)
                                    # Val2 = int(vals[1])
                                    # Val3 = int(vals[2])
                                    # Val4 = int(vals[3])
                    Channel1.append(int(numS.split(" ")[0]))
                                    # Channel1.append(Val1)
                                    # Channel2.append(Val2)
                                    # Channel3.append(Val3)
                                    # Channel4.append(Val4)
                    Time.append(i/4000/3.5)
        # print(i)
    arduino.close()
    import pandas as pd
    dict = {'Time (s)' : Time, 'Channel 1 (V)': Channel1}#,
            #'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3, 'Channel4 (V)': Channel4}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)

    return [Channel1, Time]#[Channel1,Channel2, Channel3,Channel4, Time]



import time

def collectDataMet2(COMPort, Name, AudioFileName):
    Voltage = []
    Time = []
    dataCollection = False
    dataAvailability = True
    sR = 4000/3.5
    i = 0
    j = 0
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    time.sleep(1)
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            print("start collecting")
            print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                numS = numS.split(" ")
                numS = numS[0]
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 300:
                        dataCollection = False
                    else:
                        print("Trigger")
                        dataCollection = True
                        Voltage.append(int(numS))
                        Time.append(i / sR)
                        i = i + 1
                        j = 5000/2
                        # print("StartingDataCollection")

        while dataCollection:
            line = arduino.readline()
            print(line)
            print("collecting Data")
            print(line)
            if line != (''):
                try:
                    string = line.decode()
                except:
                    print("ignored")
                else:
                    numS = string.replace("\r\n", '')
                    numS= numS.split(" ")
                    numS = numS[0]
                    print(numS)
                    if numS.isdigit():
                        if int(numS) < 300:
                            j = j - 1
                        else:
                            pass
                        Voltage.append(int(numS))
                        print(numS)
                        Time.append(i / sR)
                        i = i + 1

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Voltage}  # ,
    # 'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3, 'Channel4 (V)': Channel4}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return Voltage, Time


def collectData_multiChannel(COMPort, Period, Name):
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    Channel1 = []
    Channel2 = []
    Channel3 = []
    Channel4 = []
    Time = []
    #def animate(xVal, yVal):
    period = int(Period)
    period = period*4000
    sR = 4000/3.5
    for i in range(period):
        line = arduino.readline()

        if line != (''):
            print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                vals = numS.split(" ")
                if len(vals)>3:
                    if vals[0].isdigit():
                        if vals[1].isdigit():
                            if vals[2].isdigit():
                                if vals[3].isdigit():
                                    Channel1.append(int(vals[0]))
                                    Channel2.append(int(vals[1]))
                                    Channel3.append(int(vals[2]))
                                    Channel4.append(int(vals[3]))
                                    Time.append(i/sR)
        # print(i)
    arduino.close()
    import pandas as pd
    dict = {'Time (s)' : Time, 'Channel 1 (V)': Channel1}#,
            #'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3, 'Channel4 (V)': Channel4}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)

    return [Channel1,Channel2, Channel3,Channel4, Time]




def collectDataMet2_multiChannel(COMPort, Name, AudioFileName):
    Channel1 = []
    Channel2 = []
    Channel3 = []
    Channel4 = []
    Time = []
    dataCollection = False
    dataAvailability = True
    i = 0
    j = 0
    FirstCounter = True
    sR = 4000 / 3.5
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    if FirstCounter:
        for i in range(4000):
            print(line)
        FirstCounter = False
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            # print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 210:
                        dataCollection = False
                    else:
                        dataCollection = True
                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        if vals[3].isdigit():
                                            Channel1.append(int(vals[0]))
                                            Channel2.append(int(vals[1]))
                                            Channel3.append(int(vals[2]))
                                            Channel4.append(int(vals[3]))
                                            Time.append(i / sR)
                                            i = i + 1
                                            j = 5000
                        # print("StartingDataCollection")

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
                        if int(numS) < 210:
                            j = j - 1
                        else:
                            j = 5000

                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        if vals[3].isdigit():
                                            Channel1.append(int(vals[0]))
                                            Channel2.append(int(vals[1]))
                                            Channel3.append(int(vals[2]))
                                            Channel4.append(int(vals[3]))
                                            Time.append(i / sR)
                                            i = i + 1
                                            j = 5000

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Channel1,'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3, 'Channel4 (V)': Channel4}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return [Channel1, Channel2, Channel3, Channel4, Time]