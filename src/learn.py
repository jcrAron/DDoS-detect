import pickle
import filePath
import numpy as np
import time
import warnings

from jcraron.lib.csv import *
from jcraron.lib.path import createFileDir

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support as score


'''
from sklearn.tree import export_graphviz
import graphviz
'''


def main():
    onlyTest()
    #trainAndTest()

def onlyTest():
    print("Reading test data...")
    testMeasures,testLabels=readCsvDict(filePath.testDataProcessingFileName,iterateFunction=splitDictArray)
    print("loading model...")
    knn=pickle.load(open(filePath.knnModel,'rb'))
    dtree=pickle.load(open(filePath.dtreeModel,'rb'))
    svm=pickle.load(open(filePath.svmModel,'rb'))
    #svm=cv2.ml_SVM.load(filePath.svmModel)
    print("Predicting...")
    knnPredict(knn,testMeasures,testLabels)
    svmPredict(svm,testMeasures,testLabels)
    dtreePredict(dtree,testMeasures,testLabels)
    

def trainAndTest():
    print("Reading data...")
    trainMeasures,trainLabels=readCsvDict(filePath.trainDataProcessingFileName,iterateFunction=splitDictArray)
    testMeasures,testLabels=readCsvDict(filePath.testDataProcessingFileName,iterateFunction=splitDictArray)
    print("Training...")
    knn=knnTrain(trainMeasures,trainLabels,filePath.knnModel)
    svm=svmTrain(trainMeasures,trainLabels,filePath.svmModel)
    dtree=dtreeTrain(trainMeasures,trainLabels,filePath.dtreeModel)
    print("Predicting...")
    knnPredict(knn,testMeasures,testLabels)
    svmPredict(svm,testMeasures,testLabels)
    dtreePredict(dtree,testMeasures,testLabels)

def dtreeTrain(measures,labels,saveFile):
    dtree = DecisionTreeClassifier(criterion='gini')
    dtree = dtree.fit(measures, labels)
    createFileDir(saveFile)
    modelPickle=open(saveFile,'wb')
    pickle.dump(dtree,modelPickle)
    return dtree

def knnTrain(measures,labels,saveFile):
    '''
    @return model
    '''
    knn = KNeighborsClassifier(n_neighbors=9,p=2,n_jobs=-1)#p=1曼哈頓距離;n_jobs=-1用所有核心計算
    knn.fit(measures,labels)
    createFileDir(saveFile)
    modelPickle=open(saveFile,'wb')
    pickle.dump(knn,modelPickle)
    return knn
    
def svmTrain(measures,labels,saveFile):
    '''
    @return model
    '''
    trainMeasureMat=np.array(measures).astype("float32")
    trainLableMat=np.array(labels).astype("int32")
    
    svm=SVC(kernel='linear',probability=True,max_iter=10000)
    svm.fit(measures,labels)
    '''
    svm = cv2.ml_SVM.create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setTermCriteria((cv2.TermCriteria_COUNT+cv2.TermCriteria_EPS, 10000, 1e-16))
    svm.train(trainMeasureMat, cv2.ml.ROW_SAMPLE, trainLableMat)
    svm.save(saveFile)
    '''
    createFileDir(saveFile)
    modelPickle=open(saveFile,'wb')
    pickle.dump(svm,modelPickle)
    return svm

def svmPredict(svm,measures,trueLabels):
    '''
    @return void
    '''
    #testMeasureMat = np.array(measures).astype("float32")
    start_time=time.time()
    predictLabels = svm.predict(measures)
    end_time=time.time()
    print('svm:')
    printSorce(predictLabels,trueLabels)
    print('time:'+str((end_time - start_time)/len(trueLabels)))
    
    
def knnPredict(knn,measures,trueLabels):
    '''
    @return void
    '''
    start_time=time.time()
    predictLabels=knn.predict(measures)
    end_time=time.time()
    
    print('knn:')
    printSorce(predictLabels,trueLabels)
    print('time:'+str((end_time - start_time)/len(trueLabels)))
    

def dtreePredict(dtree,measures,trueLabels):
    '''
    @return void
    '''
    start_time=time.time()
    predictLabels=dtree.predict(measures)
    end_time=time.time()
    print('Decision Tree:')
    printSorce(predictLabels,trueLabels)
    print('time:'+str((end_time - start_time)/len(trueLabels)))
    '''
    #create graph
    dot_data = export_graphviz(dtree)
    graph = graphviz.Source(dot_data)
    graph.view()
    '''
    
def accuracy(predictLabels,trueLabels):
    correct=0
    indexLen=len(predictLabels)
    for i in range(indexLen):
        if predictLabels[i] == trueLabels[i]:
            correct+=1
    return correct/indexLen
    
def printSorce(predictLabels,trueLabels):
    print('accuracy: {}'.format(accuracy(predictLabels,trueLabels)))
    precision, recall, fscore, support = score(trueLabels, predictLabels,beta=1.0,average='binary')
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))

def splitDictArray(dictArray):
    '''
    @return dictArray [{label,other...}]
    @return (measures,labels)
    '''
    measures=[]
    labels=[]
    for dict in dictArray:
        measures.append([float(dict[title]) for title in filePath.learnTitles])
        label=int(dict[filePath.labelTitle])
        labels.append(0 if label==0 else 1)
    return (measures,labels)

#warnings.filterwarnings("ignore")
main()