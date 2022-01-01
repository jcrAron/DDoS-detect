import sys
from jcraron.lib.csv import *
import dataProcessing as dp
import matplotlib.pyplot as plt
import numpy as np
from os import environ
import filePath

def main():
    processingTrainDatas()
    processingTestDatas()
    pass

def processingTrainDatas():
    print("Start train data processing ...")
    print("Reading and Calculating datas ...")
    trainDicts=readCsvDict(filePath.originTrainFileName,iterateFunction=datasProcessing)
    print("Storing datas ...")
    writeCsvDict(filePath.trainDataProcessingFileName,trainDicts,*filePath.writeTitles)
    print("showing datas ...")
    showGraph(trainDicts,'frame.number','ip.port.src.dst.entropy')
    print("finish!")
    
def processingTestDatas():
    print("Start test data processing ...")
    print("Reading and Calculating datas ...")
    testDicts=readCsvDict(filePath.originTestFileName,iterateFunction=datasProcessing)
    print("Storing datas ...")
    writeCsvDict(filePath.testDataProcessingFileName,testDicts,*filePath.writeTitles)
    print("showing datas ...")
    showGraph(testDicts,'frame.number','ip.port.src.dst.entropy')
    print("finish!")

def showGraph(dictArray,xTitle,yTitle):
    plt.cla()
    colorDict={0:'k',1:'g',2:'b',3:'r'}
    labelDict={0:'normal',1:'udp',2:'syn',3:'icmp'}
    datas={}
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    for dataDict in dictArray:
        '''
        if dataDict['label']==3:
            continue
        '''
        x,y=datas.setdefault(dataDict['label'],([],[]))
        x.append(dataDict[xTitle])
        y.append(dataDict[yTitle])
    for label,value in datas.items():
        x,y=value
        plt.scatter(x,y,color=colorDict[label],marker='.',label=labelDict[label])#scatter alpha
    plt.legend(loc='best')
    plt.show()
    

def datasProcessing(rows):
    '''
    @param dicts an array of dict
    @return an array of dict
    '''
    retArray=[]
    probDict={}
    info={}
    for row in rows:
        row['srcport']=row['tcp.srcport'] if row['tcp.srcport']!= '' else row['udp.srcport']
        row['dstport']=row['tcp.dstport'] if row['tcp.dstport']!= '' else row['udp.dstport']
        if row['srcport']=='':
            row['srcport']='0'
        if row['dstport']=='':
            row['dstport']='0'
        con=False
        for key in row:
            if key in filePath.readTitles and row[key]=='':
                con=True
                break
        if con :
            continue
        dict=dp.dataProcessing({k:v for k,v in row.items() if k in filePath.readTitles},0.1,info)
        retArray.append(dict)
    return retArray


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()
main()