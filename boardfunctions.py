import numpy 

# Speicher für den Zustand des Bretts
sm=[]
sm=numpy.zeros((6,7))

def converttostyledict(inputsm):
    newdict={}
    stylemap={0.0:'chips grau',1.0:'chips rot',2.0:'chips gelb'}
    for xkey, row in dict(enumerate(inputsm)).items():
        for ykey, value in dict(enumerate(row)).items():
            newdict[str(xkey)+str(ykey)]=stylemap[value] 
    return newdict

def converttoouputlist(inputsm):
    newlist=[]
    stylemap={0.0:'chips grau',1.0:'chips rot',2.0:'chips gelb'}
    for xkey, row in dict(enumerate(inputsm)).items():
        for ykey, value in dict(enumerate(row)).items():
            newlist.append(stylemap[value])
    return newlist

# print(converttostyledict(sm))
# print(list(enumerate(sm)))
# print(sm.tolist())

