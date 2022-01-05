#https://blog.gtwang.org/programming/python-csv-file-reading-and-writing-tutorial/
#read dataset and make entropy file

import math
from scipy.stats import norm
import numpy as np

def ipToNum(ip):
    '''
    @param String; ip=X0.X1.X2.X3 
    @return int; X0*16777216+X1*65536+X2*256+X3
    '''
    ipSplit=[int(str) for str in ip.split('.') if str != '']
    return ipSplit[0]*(16777216)+ipSplit[1]*(65536)+ipSplit[2]*256+ipSplit[3]
    
def portToNum(port):
    return int(port)
    
def labelToNum(label):
    '''
    @return int
    '''
    if label=="normal":
        return 0
    elif label=="udp":
        return 1
    elif label=="syn":
        return 2
    elif label=="icmp":
        return 3
    else:
        raise Exception("unknow label")


def dataProcessing(data,timeInterval,info):
    '''
    @param data dict{String:String}
    @param timeInterval calculate entropy per timeInterval
    @param info 
    @return dict
    '''
    
    dict={}
    number=info.setdefault('frame.number',1)
    dict['frame.number']=number
    info['frame.number']+=1
    
    dict['frame.time_relative']=float(data['frame.time_relative'])
    nowTime= float(dict['frame.time_relative'])
    lastTime=info.setdefault('time.last',0)
    isNewInterval=False
    if abs(nowTime-lastTime)>=timeInterval:
        isNewInterval=True
        info['time.last']=nowTime
    entropyInfos=info.setdefault('entropyInfos',{});
    dict['label']=labelToNum(data['label'])
    
    
    entropyBykey = lambda key,tonum:defaultCalcEntropy(tonum(data[key]),entropyInfos.setdefault(key,{}),isNewInterval)
    dict['ip.src.entropy']=entropyBykey('ip.src',ipToNum)
    dict['ip.dst.entropy']=entropyBykey('ip.dst',ipToNum)
    dict['srcport.entropy']=entropyBykey('srcport',portToNum)
    dict['dstport.entropy']=entropyBykey('dstport',portToNum)
    
    entropy = lambda data,key:defaultCalcEntropy(data,entropyInfos.setdefault(key,{}),isNewInterval)
    dict['ip.port.src.dst.entropy']=entropy((data['ip.src'],data['srcport'],data['ip.dst'],data['dstport']),'ip.port.src.dst.entropy')
    
    
    #calcEntropy((data['ip.src'],data['srcport']),probDict.setdefault('ipport.entropy',{}))
    #dict['ip.port.entropy']=calcEntropy_ZongLunLi(data,entropyInfos.setdefault('ip.port',{}))
    
    #dict['ipport.entropy']=calcEntropy_v2(data,info.setdefault("ipport.entropy",{}))
    dict['ip.proto']=normalize(int(data['ip.proto']))
    return dict

def normalize(num):
    return math.tanh(num*0.1)
    #return num
    
def gaussian(list):
    mean,stdev=norm.fit(list)
    return norm(mean,stdev);

def calcEntropy_v2(newData,info):
    '''
    "A DDoS Attack Mitigation Scheme in ISP Networks Using Machine Learning Based on SDN"
    @param newData whole packet
    '''
    return calcEntropy_v1(newData['srcport'],info.setdefault(newData['ip.src'],{}))

def calcEntropy_v1(newData,info,isNewInterval):
    '''
    @param newData Object
    @return float
    '''
    if isNewInterval:
        info['counter']={}
        info['totalCount']=0
        info['mean']={}
        info['stdev']={}
        pass
    counter=info.setdefault("counter",{})
    valueTotal=info['totalCount']=info.setdefault("totalCount",0)+1
    counter[newData]=counter.setdefault(newData,0)+1
    entropy=-sum([(value/valueTotal)*math.log(value/valueTotal,2) for value in counter.values()])
    mean,stdev=calcMean(entropy,info.setdefault("mean",{})),calcStdev(entropy,info.setdefault("stdev",{}))
    if stdev==0:
        return 0
    return math.tanh(0.1*(entropy-mean)/stdev)
    
def calcStdev(newData,info):
    '''
    ((sum(x**2)-(sum(x)**2)/total)/total)**(0.5)
    @param newData number
    '''
    sumx=info['sumx']=info.setdefault('sumx',0)+(newData) #sum(x)
    powx=info['powx']=info.setdefault('powx',0)+(newData**2) #sum(x**2)
    total=info['total']=info.setdefault('total',0)+1
    return ((powx-(sumx**2)/total)/total)**(0.5)

def calcMean(newData,info):
    '''
    @param newData number
    '''
    sumx=info['sumx']=info.setdefault('sumx',0)+(newData) #sum(x)
    total=info['total']=info.setdefault('total',0)+1
    return sumx/total


def calcEntropy_ZongLunLi(newData,info):
    '''
    @param newData whole packet
    @return float
    '''
    ip=ipToNum(newData['ip.src'])
    port=portToNum(newData['srcport'])
    
    arr=info.setdefault("counter",{}).setdefault(ip,[0,{}])
    portCounters=arr[1]
    portCounters[port]=portCounters.setdefault(port,0)+1
    
    if portCounters[port]<=1:
        return 0
    arr[0]+=1
    totalCount=arr[0]
    p=portCounters[port]/totalCount
    entropy=-p*math.log(p,10)
    
    portAmount=len(portCounters)
    mean=totalCount / portAmount
    oo=0
    for value in portCounters.values():
        oo += (value - mean) ** 2
        oo = (oo / totalCount) ** (1/2)
    return math.tanh(0.1 * (entropy - mean) / oo)

defaultCalcEntropy=calcEntropy_v1