import matplotlib.pyplot as plt



def main():
    print("Reading and Calculating datas ...")
    dicts=readCsvDict(filePath.trainDataProcessingFileName,iterateFunction=datasProcessing)
    print("showing datas ...")
    showGraph(dicts,'frame.number','ip.src.entropy')
    pass

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
    
    
main()