import connectfour
import brutalcomputer

cf=connectfour.Connectfour()
res=-1
reslist=[]
while res==-1:
    bc = brutalcomputer.Brutalcomputer(cf,k=4)
    slot=bc.nextturn(method="brutal")
    print(slot)
    cf.doturn(slot,countseq=False,saveoneturn=False,computer=False)
    res=cf.endresult
reslist.append(res)
cf.print()

