import numpy as np
import pandas as pd
import brutalcomputer
import logging
logging.info('Connectfour is loaded')

# solution by https://stackoverflow.com/questions/74178272/numpy-diagonal-function-is-slow?noredirect=1#comment130970516_74178272   
known_diagonals = dict()
def diagonal_indices(h: int, w: int, length: int = 3) -> np.array:
    '''
    Returns array (shape diagonal_count x length) of diagonal indices
    of a flatten array
    '''
    # one of many ways to store precomputed function output
    # cleaner way would probably be to do this outside this function
    diagonal_indices_key = (h, w, length)
    if diagonal_indices_key in known_diagonals:
        return known_diagonals[diagonal_indices_key]
    
    diagonals_count = (h + 1 - length) * (w + 1 - length) * 2

    # default value is meant to ease process with cumsum:
    # adding h + 1 selects an index 1 down and 1 right, h - 1 index 1 down 1 left
    # firts half dedicated to right down diagonals
    diagonals = np.full((diagonals_count, length), w + 1, dtype=np.int32)
    # second half dedicated to left down diagonals
    diagonals[diagonals_count//2::] = w - 1

    # this could have been calculated mathematicaly
    flat_indices = np.arange(w * h).reshape((h, w))
    # print(flat_indices)

    # selects rectangle offseted by l - 1 from right and down edges
    diagonal_starts_rd = flat_indices[:h + 1 - length, :w + 1 - length]
    # selects rectangle offseted by l - 1 from left and down edges
    diagonal_starts_ld = flat_indices[:h + 1 - length, -(w + 1 - length):]
    
    # sets starts
    diagonals[:diagonals_count//2, 0] = diagonal_starts_rd.flatten()
    diagonals[diagonals_count//2::, 0] = diagonal_starts_ld.flatten()

    # sum triplets left to right
    # diagonals contains triplets (or vector of other length) of (start, h+-1, h+-1). cumsum makes diagonal indices
    diagonals = diagonals.cumsum(axis=1)

    # save ouput
    known_diagonals[diagonal_indices_key] = diagonals

    return diagonals


class Connectfour:
    def reset(self):
        logging.debug('reset cf object')
        # matrix to store the board's status
        self.sm=np.zeros((6,7),dtype=np.int8)
        # 1: red, 2: yellow's turn, red starts
        self.turn=1     
        self.slotid=-1
        self.turnid=-1
        self.gameid+=1
        # -1: still running, 1: red, 2: yellow, 3: tie
        self.endresult=-1
        # nmber of sequences for each color: red,yellow and possible sequences 2,3,4
        self.scount=np.zeros((2,3),dtype=np.int8)
        # a weighted score for red an yellow sequences
        self.score=np.zeros(2,dtype=np.int8)
        # net score
        self.netscore=0

    def __init__(self,cf=None,mode="player vs computer",k=2):
        self.gameid=1
        # game mode for player vs. player option
        self.mode=mode
        # the search depth of the computer enemy
        self.k=k
        # reset function should not wipe the memory, so it's not in reset function
        self.storage=pd.DataFrame(columns=[ "gameid",
                                            "turnid",
                                            "slotid",
                                            "sm",
                                            "scount",
                                            "score",
                                            "netscore",
                                            "endresult"])
        self.reset()
        if isinstance(cf,Connectfour):
            self.sm=np.copy(cf.sm)
            self.turn=cf.turn

    def print(self):
        print(self.sm)
        print("turn: ","red" if self.turn==1 else "yellow")
        print("turnid: ",self.turnid)
        print("endresult: ",self.endresult)

    # Save one turn to the pandas DataFrame
    def saveoneturn(self):
        newrow=pd.DataFrame([[
            self.gameid,
            self.turnid,
            self.slotid,
            # the constructor and the list are needed, so that it's stored as object in pandas
            [np.array( self.sm )],
            [np.array( self.scount)],
            [np.array( self.score)],
            self.netscore,
            self.endresult]],
            columns=[ "gameid",
                       "turnid",
                       "slotid",
                       "sm",
                       "scount",
                       "score",
                       "netscore",
                       "endresult"]
        )
        self.storage=pd.concat([self.storage,newrow])
        # print(self.storage)
    
    def writetodisk(self,format="csv",file="storage"):
        print("write to: "+file)
        if format=="csv":
            self.storage.to_csv(file+".csv")
        elif format=="feather":
            self.storage.to_feather(file+".ftr")

    # Do one turn based on selected colum
    # and return whether it was an acceptable move
    def doturn(self,col,countseq=True,saveoneturn=True,computer=True)->int:
        if self.endresult>0:
            return 0

        c=self.sm[:,col]
        firstincol=np.argmax(c>0)-1 if (c>0).any() else 5
        # only if this is an acceptable move
        if firstincol>=0:
            self.sm[firstincol,col]=self.turn
            self.slotid=col
            self.turnid+=1
            if countseq:
                self.countseq(redyellow=self.turn)
            if self.findfour(redyellow=self.turn):
                self.endresult=self.turn
            elif self.sm.all():
                # all chips are filled, but no 4ers: tie
                self.endresult=3
            if saveoneturn:
                self.saveoneturn()
            if self.endresult<0:
                self.turn=2 if self.turn==1 else 1
                if self.mode=="player vs computer" and computer==True and self.turn==2:
                    bc = brutalcomputer.Brutalcomputer(self,k=self.k)
                    self.doturn(bc.nextturn(method="brutal"),countseq=countseq,saveoneturn=saveoneturn)
            return 1
        else:
            return -1

    def findfour(self, redyellow: int=1)->bool:
        return self.findseq(seq=4,redyellow=redyellow)>0
    
    def countseq(self, redyellow: int=1):
        rllist=[1,2] if redyellow==3 else [redyellow]
        for redyellowi in rllist:
            for seqc in range(3):
                x=self.findseq(seq=seqc+2,redyellow=redyellowi)
                self.scount[redyellowi-1][seqc]=x
        self.score=(self.scount*np.array([2,5,1000])).sum(axis=1)
        self.netscore=self.score[0]-self.score[1]

    def findseq(self , seq: int =2, redyellow: int=1) -> int:
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

        # find the diagonals
        diagonals = diagonal_indices(*self.sm.shape, seq)
        seqmat = np.all(self.sm.flatten()[diagonals] == redyellow, axis=1)
        matches += seqmat.sum()
        return matches

    def randomdebug(self):
        self.sm=np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,2,1,1,0,0]])
        self.sm=np.random.randint(0,3,size=(6,7))
        
        # # search in the diagonals
        # diags=np.zeros((1,6),dtype=np.int8)
        # for k in range(-5,7):   
        #     t=np.zeros(6,dtype=np.int8)
        #     a=np.diag(self.sm,k=k).copy()
        #     t[:len(a)] += a
        #     s=np.zeros(6,dtype=np.int8)
        #     a=np.diag(np.fliplr(self.sm),k=k).copy()
        #     s[:len(a)] += a
        #     diags=np.concatenate(( diags,t[None,:],s[None,:]),axis=0)
        # # same pattern as above for horizontal applied to diagonal sequences
        # diags=np.delete(diags,0,0)
        # Na=np.size(diags,axis=1)
        # n=np.arange(Na-seq+1)[:,None]+np.arange(seq)
        # seqmat=np.all(diags[:,n]==redyellow,axis=2)
        # matches+=seqmat.sum()

        return matches

    def converttoouputlist(self):
        """Convert the status to a list of classnames for output in dash
        
        the list iterates through the board like reading a text
        starting from upper left, line by line
        newlist=[]
        """
        stylemap={0:'chips grau',1:'chips rot',2:'chips gelb'}
        for _, row in dict(enumerate(self.sm)).items():
            for _, value in dict(enumerate(row)).items():
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


