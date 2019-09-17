def correctPathXML(path):
    splittedPath = path.split(' ')
    finalPath = '"'
    for i in splittedPath:
        finalPath += (i + '&#32;')
    return finalPath[:-5] + '"'

def correctPath(path):
    splittedPath = path.split(' ')
    finalPath = ''
    for i in splittedPath:
        finalPath += (i + '\ ')
    return finalPath[:-2]

def isEmpty(inputText):
    if inputText == '':
        return True
    return False