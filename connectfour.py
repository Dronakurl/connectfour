import numpy as np
import pandas as pd

class Connectfour:
    def reset(self):
        # matrix to store the board's status
        self.sm=np.zeros((6,7),dtype=np.uint8)
        # 1: red, 2: yellow's turn, red starts
        self.turn=1     
        self.slotid=-1
        self.turnid=-1
        self.gameid+=1
        # -1: still running, 1: red, 2: yellow, 3: tie
        self.endresult=-1
        # number of sequences for each color: red,yellow and possible sequences 2,3,4
        self.scount=[[0]*3 for i in range(2)]

    def __init__(self):
        self.gameid=1
        # reset function should not wipe the memory, so it's not in reset function
        self.storage=pd.DataFrame(columns=[ "gameid",
                                            "turnid",
                                            "slotid",
                                            "sm",
                                            "seqred2",
                                            "seqred3",
                                            "seqred4",
                                            "seqyel2",
                                            "seqyel3",
                                            "seqyel4",
                                            "endresult"])
        self.reset()

    def print(self):
        print("state of the board: ",self.sm)
        print("turn: ","red" if self.turn==1 else "yellow")
        print("turnid: ",self.turnid)

    # Save one turn to the pandas DataFrame
    def saveoneturn(self):
        newrow=pd.DataFrame([[
            self.gameid,
            self.turnid,
            self.slotid,
            [np.array( self.sm )],
            *self.scount[0],
            *self.scount[1],
            self.endresult]],
            columns=[ "gameid",
                       "turnid",
                       "slotid",
                       "sm",
                       "seqred2",
                       "seqred3",
                       "seqred4",
                       "seqyel2",
                       "seqyel3",
                       "seqyel4",
                       "endresult"]
        )
        self.storage=pd.concat([self.storage,newrow])
        print(self.storage)
    
    def writetodisk(self,format="csv",file="storage"):
        print("write to: "+file)
        if format=="csv":
            self.storage.to_csv(file+".csv")
        elif format=="feather":
            self.storage.to_feather(file+".ftr")

    # Do one turn based on selected colum
    # and return whether it was an acceptable move
    def doturn(self,col):
        if self.endresult>0:
            return 0

        c=self.sm[:,col]
        firstincol=np.argmax(c>0)-1 if (c>0).any() else 5
        # only if this is an acceptable move
        if firstincol>=0:
            self.sm[firstincol,col]=self.turn
            self.slotid=col
            self.turnid+=1
            self.countseq(redyellow=self.turn)
            if self.findfour(redyellow=self.turn):
                self.endresult=self.turn
            elif self.sm.all():
                self.endresult=3
            self.saveoneturn()
            if self.endresult<0:
                self.turn=2 if self.turn==1 else 1
            return 1
        else:
            return -1

    def findfour(self,redyellow=1):
        return self.findseq(seq=4,redyellow=redyellow)>0
    
    def countseq(self,redyellow=1):
        rllist=[1,2] if redyellow==3 else [redyellow]
        for redyellowi in rllist:
            for seqc in range(3):
                x=self.findseq(seq=seqc+2,redyellow=redyellowi)
                # print("redyellowi,seq",redyellowi,seqc,x)
                self.scount[redyellowi-1][seqc]=x
        # self.print()
        # print(self.scount)

    def findseq(self,seq=2,redyellow=1):
        matches=0
        # search horizontally and vertically
        for axis in [0,1]:
            Na=np.size(self.sm,axis=axis)
            # possible indices of sequences
            n=np.arange(Na-seq+1)[:,None]+np.arange(seq)
            # search 3D array of all possible sequences for sequences
            if axis==1:
                seqmat=np.all(self.sm[:,n]==redyellow,axis=2)
            else:
                seqmat=np.all(self.sm[n,:]==redyellow,axis=1)
            matches+=seqmat.sum()
        
        # search in the diagonals
        diags=np.zeros((1,6),dtype=np.uint8)
        for k in range(-5,7):   
            t=np.diag(self.sm,k=k).copy()
            t.resize(6)
            s=np.diag(np.fliplr(self.sm),k=k).copy()
            s.resize(6)
            diags=np.concatenate(( diags,t[None,:],s[None,:]),axis=0)
        # same pattern as above for horizontal applied to diagonal sequences
        diags=np.delete(diags,0,0)
        Na=np.size(diags,axis=1)
        n=np.arange(Na-seq+1)[:,None]+np.arange(seq)
        seqmat=np.all(diags[:,n]==redyellow,axis=2)
        matches+=seqmat.sum()

        # print("finding seq for: ",redyellow)
        # print("matches:",matches)
        return matches

    def randomdebug(self):
        self.sm=np.random.randint(0,3,size=(6,7))
        self.sm=np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,2,1,1,0,0]])

    # convert the status to a list of classname for output in dash
    #   the list iterates through the board like reading a text
    #   starting from upper left, line by line
    def converttoouputlist(self):
        newlist=[]
        stylemap={0:'chips grau',1:'chips rot',2:'chips gelb'}
        for xkey, row in dict(enumerate(self.sm)).items():
            for ykey, value in dict(enumerate(row)).items():
                newlist.append(stylemap[value])
        return newlist

    # convert the info, whose turn it is, to a style for the dash gui
    def turntostyle(self):
        if self.endresult==-1:
            if self.turn==1:
                return {"background-color":"#D50000"},"red's turn"
            elif self.turn==2:
                return {"background-color":"#DBDD00"},"yellow's turn"
        elif self.endresult==3:
            return {"background-color":"green"},"tie!"
        elif self.endresult==1:
            return {"background-color":"green"},"red won!" 
        elif self.endresult==2:
            return {"background-color":"green"},"yellow won!" 
        else:
            return {"background-color":"red"},"ERROR" 



# c=Connectfour()
# c.randomdebug()
# c.print()
# c.countseq(redyellow=3)
# c.doturn(col=1)
# c.doturn(col=4)

# print("2 of 1 ",c.findseq(seq=2,redyellow=1))
# print("3 of 1 ",c.findseq(seq=3,redyellow=1))
# print("3 of 1 ",c.findseq(seq=3,redyellow=1))
# print("3 of 2 ",c.findseq(seq=3,redyellow=2))
