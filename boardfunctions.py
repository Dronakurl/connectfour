import numpy 

# Speicher für den Zustand des Bretts
sm=[]
sm=numpy.zeros((7,6))

def converttostyledict(inputsm):
    dict(enumerate(inputsm.flatten(), 1))

print(convertostyledict(sm))


