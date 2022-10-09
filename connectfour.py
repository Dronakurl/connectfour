import numpy as np
import pandas as pd

class Connectfour:
    def reset(self):
        # matrix to store the board's status
        self.sm=np.zeros((6,7))
        # whos turn is it, red (1.0) starts
        self.turn=1.0

    def __init__(self):
        self.reset()

    def print(self):
        print(self.sm)

    # Do one turn based on selected colum
    def doturn(self,col):
        c=self.sm[:,col]
        firstincol=np.argmax(c>0)-1 if (c>0).any() else 5
        if firstincol>0:
            self.sm[firstincol,col]=self.turn
        self.turn=2.0 if self.turn==1.0 else 1.0

    # convert the status to a list of classname for output in dash
    #   the list iterates through the board like reading a text
    #   starting from upper left, line by line
    def converttoouputlist(self):
        newlist=[]
        stylemap={0.0:'chips grau',1.0:'chips rot',2.0:'chips gelb'}
        for xkey, row in dict(enumerate(self.sm)).items():
            for ykey, value in dict(enumerate(row)).items():
                newlist.append(stylemap[value])
        return newlist

    # convert the info, whose turn it is, to a style for the dash gui
    def turntostyle(self):
        stylemap={0.0:{"background-color":"grey"},1.0:{"background-color":"red"},2.0:{"background-color":"yellow"}}
        return stylemap[self.turn]

