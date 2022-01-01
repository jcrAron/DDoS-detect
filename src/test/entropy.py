import math,os
import matplotlib.pyplot as plt

prob={}
def calcEntropy(newData,prob):
    '''
    @param prob dict{data,count}
    @return float
    '''
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html
    if newData in prob:
        prob[newData]+=1
    else:
        prob[newData]=1
    vs=prob.values()
    valueTotal=sum(vs)
    ps=[v/valueTotal for v in vs]
    return -sum([p*math.log(p,2) for p in ps])

def show(datas):
    '''
    @param number[]
    '''
    plt.plot([i for i in range(len(datas))],datas,'ro')
    plt.show()

def initProb():
    global prob
    prob={}
    print('prob is inited')
    
def cls():
    os.system('cls')
    print('useful function: cls()')
    print('useful function: initProb()')
    print('useful function: batchCalc(*datas)')
    print('useful function: show(datas)')
    print('useful function: calcEntropy(newData,prob)')
    

batchCalc=lambda *datas:[calcEntropy(data,prob) for data in datas]

cls()