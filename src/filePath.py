from jcraron.lib.path import *

readTitles=['frame.number','frame.time_relative','ip.proto','ip.src','ip.dst','srcport','dstport','label']

labelTitle='label'
learnTitles=['ip.proto','ip.src.entropy','ip.dst.entropy','srcport.entropy','dstport.entropy','ip.port.src.dst.entropy']
writeTitles=['frame.number','frame.time_relative',labelTitle]+learnTitles

originTrainFileName=pathJoins('datas','origin','network_data_train.csv')
trainDataProcessingFileName=pathJoins('datas','entropy','network_data_train.csv')

originTestFileName=pathJoins('datas','origin','network_data_test.csv')
testDataProcessingFileName=pathJoins('datas','entropy','network_data_test.csv')

knnModel=pathJoins('datas','model','knn.model')
svmModel=pathJoins('datas','model','svm.model')
dtreeModel=pathJoins('datas','model','clf.model')
