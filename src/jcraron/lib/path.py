import os


def getAllFile(rootDir):
    '''
    @return rootDir String
    @return String[]
    '''
    ret = []
    for file in os.listdir(rootDir):
        filePath = pathJoin(rootDir, file)
        if os.path.isdir(filePath):
            ret += getAllFile(filePath)
        else:
            ret.append(filePath)
    return ret

def createFileDir(file):
    absFile=os.path.abspath(file)
    if os.path.exists(absFile):
        return
        
    dirname=os.path.dirname(absFile)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        

def pathJoin(dir, file, delimiter="\\"):
    '''
    @param file String
    @param delimiter String; default:"\\\\"
    @return String
    '''
    return os.path.normpath(dir) + delimiter + file


def pathJoins(dir, *dirs, delimiter="\\"):
    '''
    @param dir String;the parent path
    @param delimiter String; default:"\\\\"
    @return String
    @example pathJoins("dir1","dir2","dir3")=="dir1\\dir2\\dir3"
    '''
    name = dir
    for path in dirs:
        name = pathJoin(name, path,delimiter)
    return name