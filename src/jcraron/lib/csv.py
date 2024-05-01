import csv
from ..lib.path import createFileDir

def toArray(rows):
    '''
    @return string array
    '''
    retArray=[]
    for row in rows:
        retArray.append(row)
    return retArray

def readCsvList(fileName,iterateFunction=toArray):
    '''
    @param fileName string
    @param iterateFunction(rows); rows type is an iterator of list
    @return iterateFunction return
    '''
    with open(fileName, newline='') as csvfile:
        rows = csv.reader(csvfile)
        return iterate(rows)

def writeCsvList(fileName,table):
    '''
    @param fileName string
    @param table 2D array
    '''
    createFileDir(fileName)
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)
      
def readCsvDict(fileName,iterateFunction=toArray):
    '''
    @param fileName string
    @param iterateFunction(rows); rows type is an array of dict
    @return iterateFunction return
    '''
    with open(fileName, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        return iterateFunction(rows)

def writeCsvDict(fileName,dicts,*fieldnames):
    '''
    @param fileName string
    @param dicts an array of Dictionary
    @example writeCsvDict("file",{a:1,b:2,c:3},"a","b")
    '''
    createFileDir(fileName)
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dicts)