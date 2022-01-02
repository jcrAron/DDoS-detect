import matplotlib.pyplot as plt
import filePath
from jcraron.lib.csv import *
from os import environ

def main():
    print("Reading datas ...")
    dicts=readCsvDict(filePath.trainDataProcessingFileName)
    print("showing datas ...")
    for title in filePath.learnTitles:
        showGraph(dicts,'frame.number',title)
    pass

def showGraph(dictArray,xTitle,yTitle):
    plt.cla()
    '''
    colorDict={0:'k',1:'g',2:'b',3:'r'}
    labelDict={0:'normal',1:'udp',2:'syn',3:'icmp'}
    '''
    colorDict={0:'k',1:'g'}
    labelDict={0:'normal',1:'attack'}
    datas={}
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    for dataDict in dictArray:
        '''
        if dataDict['label']==3:
            continue
        '''
        label=int(dataDict['label'])
        label=0 if label==0 else 1 
        x,y=datas.setdefault(label,([],[]))
        x.append(float(dataDict[xTitle]))
        y.append(float(dataDict[yTitle]))
    for label,value in datas.items():
        x,y=value
        plt.scatter(x,y,color=colorDict[label],marker='.',label=labelDict[label])#scatter alpha
    plt.legend(loc='best')
    plt.show()
    
    
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
main()