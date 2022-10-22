import numpy as np
import pandas as pd
import connectfour
import random

class Brutalcomputer:
    def __init__(self,cf=None,k=2):
        if cf is None:
            self.sf=connectfour.Connectfour()
        else:
            # initialized Connectfour object, but with a pre-filled board state
            self.sf=connectfour.Connectfour(cf)
        # Copy the original board state that is the basis for the next turn
        self.sm_orig=self.sf.sm.copy()
        # only used temporarly for the recursive calculation of the tree
        self.slothist=[]
        # matrix to store the search tree results
        self.brutalmatrix=None
        # tree depth for the brute search
        self.k = k

    def print(self):
        print("########## print Brutalcomputer ##############")
        print(self.sf.sm)
        print(self.brutalmatrix)
        print("##############################################")

    def nextturn(self,method="random"):
        if method=="random":
            return random.randint(0,6)
        elif method=="brutal":
            self.calcposs(k=self.k)
            return self.findbestbranch()

    def findbestbranch(self):
        gc=self.brutalmatrix
        for ik in range(self.k-1):
            groupcol=gc.columns.values.tolist()[0:-2]
            dropcol=gc.columns.values.tolist()[-2:-1]
            # print("######## k #####",ik,self.k,((self.k-ik-1) % 2) )
            if ((self.k-ik-1) % 2) != 0: 
                gc=gc.drop(dropcol,axis=1).groupby(groupcol).min().reset_index()
            else:
                gc=gc.drop(dropcol,axis=1).groupby(groupcol).max().reset_index()
            # print(gc)
            # print("################")
        return gc.sort_values("netscore",ascending=False).reset_index().loc[0,0]

    def calcposs(self,k=1):
        for possmove in range(7):
            smcp=self.sf.sm.copy()
            turncp=self.sf.turn
            # ignore impossible moves
            if self.sf.doturn(col=possmove,saveoneturn=False,countseq=False)==1:
                self.slothist.append(possmove)

                # print("debug in possmove",k, possmove)
                # print(self.sf.sm)
                # print(self.sf.turn)
                # print("end debug in possmove")

                # move one level deeper if not on maximum level and if tree doesn't end here
                if k-1>0 and self.sf.endresult<0: 
                    self.calcposs(k=k-1)
                else:
                    # placeholder history for data collection
                    for ki in range(k-1):
                        self.slothist.append(-1)
                    # at the end of the iteration tree, count and collect data
                    self.sf.countseq(redyellow=3)
                    newl=pd.DataFrame([[*self.slothist,self.sf.netscore]])
                    newl.columns=[*range(len(self.slothist)),"netscore"]
                    if self.brutalmatrix is None:
                        self.brutalmatrix=newl
                    else:
                        self.brutalmatrix=pd.concat([self.brutalmatrix,newl])
                    for ki in range(k-1):
                        self.slothist.pop()

                    # print("slothist: ",self.slothist)
                    # print("score: ",self.sf.scount)
                    # print(self.brutalmatrix)

                self.sf.sm=smcp
                self.sf.turn=turncp
                self.sf.endresult=-1
                self.slothist.pop()

