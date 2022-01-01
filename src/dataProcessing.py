#https://blog.gtwang.org/programming/python-csv-file-reading-and-writing-tutorial/
#read dataset and make entropy file

import math
from scipy.stats import norm
import numpy as np

def ipToNum(ip):
    '''
    @param String; ip=X0.X1.X2.X3 
    @return int; X0*1000+X1*100+X2*10+X3
    '''
    ipSplit=[int(str) for str in ip.split('.') if str != '']
    return ipSplit[0]*1000+ipSplit[1]*100+ipSplit[2]*10+ipSplit[3]
    
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
    entropyBykey = lambda key,tonum:normalize(defaultCalcEntropy(tonum(data[key]),entropyInfos.setdefault(key,{}),isNewInterval))
    dict['ip.src.entropy']=entropyBykey('ip.src',ipToNum)
    dict['ip.dst.entropy']=entropyBykey('ip.dst',ipToNum)
    dict['srcport.entropy']=entropyBykey('srcport',portToNum)
    dict['dstport.entropy']=entropyBykey('dstport',portToNum)
    
    entropy = lambda data,key:normalize(defaultCalcEntropy(data,entropyInfos.setdefault(key,{}),isNewInterval))
    dict['ip.port.src.dst.entropy']=entropy((data['ip.src'],data['srcport'],data['ip.dst'],data['dstport']),'ip.port.src.dst.entropy')
    
    #calcEntropy((data['ip.src'],data['srcport']),probDict.setdefault('ipport.entropy',{}))
    #dict['ip.port.entropy']=calcEntropy_ZongLunLi(data,entropyInfos.setdefault('ip.port',{}))
    
    dict['ip.proto']=normalize(int(data['ip.proto']))
    return dict

def normalize(num):
    return math.tanh(num*0.1)
    #return num
    
def gaussian(list):
    mean,stdev=norm.fit(list)
    return norm(mean,stdev);

def calcEntropy_gaussian(newData,info,isNewInterval):
    '''
    @deprecated too slow
    @param newData int
    @return float
    '''
    if isNewInterval:
        info['norm']=gaussian(info['list'])
        info['list']=[]
    list=info.setdefault("list",[])
    list.append(newData)
    if not 'norm' in info.keys():
        return 0
    ps=[norm.pdf(v) for v in list]
    return -sum([p*math.log(p,2) for p in ps])
    


def calcEntropy_section(newData,info,isNewInterval):
    '''
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html
    @param newData Object
    @return float
    '''
    if isNewInterval:
        info['counter']={}
        pass
    counter=info.setdefault("counter",{})
    counter[newData]=counter.setdefault(newData,0)+1  
    vs=counter.values()
    valueTotal=sum(vs)
    ps=[v/valueTotal for v in vs]
    return -sum([p*math.log(p,2) for p in ps])
    

def calcEntropy_slideWindow(newData,info,isNewInterval):
    '''
    "Statistical Approaches to DDoS Attack Detection and Response"?
    @deprecated
    @param newData Object
    @return float
    '''
    queue=info.setdefault("queue",[])
    queue.insert(0,newData)
    size=100
    if len(queue)>size:
        queue.pop()
    else:
        return 0
    ps=[queue.count(newData)/size for data in set(queue)]
    return -sum([p*math.log(p,2) for p in ps])


def calcEntropy_noSum(newData,info,isNewInterval):
    '''
    @deprecated
    @param newData Object
    @return float
    '''
    if isNewInterval:
        #info['counter']={}
        #info['tatalCount']=0
        pass
    counter=info.setdefault("counter",{})
    counter[newData]=counter.setdefault(newData,0)+1
    info['tatalCount']=info.setdefault('tatalCount',0)+1
    valueTotal=info['tatalCount']
    p=counter[newData]/valueTotal
    return -p*math.log(p,2)

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

defaultCalcEntropy=calcEntropy_section