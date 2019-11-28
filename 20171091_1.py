import sys

def readinput(file):
    """
    Returns contents of disk and transactions
    """

    Disk,Tran=[{},{}]
    
    with open(file,'r') as f:

        #read first line
        fl=f.readline()
        fl=fl.strip().split()

        for i in range(0,len(fl),2):
            Disk[fl[i]]=fl[i+1]

        # print(Disk)

        #read transactions
        flag=0
        tr=0
        for line in f:
            line=line.strip().split()
            if(len(line)==0):
                flag=1
            else:
                if(flag):
                    Tran[line[0]]=[]
                    tr=line[0]
                    flag=0
                else:
                    Tran[tr].append(line)

        # for x in Tran:
        #     print (x)
        #     for y in Tran[x]:
        #         print(y)

    return [Disk,Tran]



def str_to_list(tr,v):
    """
    Convert string to list
    """

    if(v=="r"):
        tr=tr[5:]
        tr=tr[:-1]
        tr=tr.split(",")
        return tr

    if(v=="w"):
        tr=tr[6:]
        tr=tr[:-1]
        tr=tr.split(",")
        return tr

    if(v=="o"):
        tr=tr[7:]
        tr=tr[:-1]
        tr=tr.split(",")
        return tr



def evalexp(e,var):
    """
    Check which op to perform
    """
    
    if(len(e[2].split('+'))==2):
        var[e[0]]=evalexp2(e[2],'+',var)
    
    if(len(e[2].split('-'))==2):
        var[e[0]]=evalexp2(e[2],'-',var)    
    
    if(len(e[2].split('/'))==2):
        var[e[0]]=evalexp2(e[2],'/',var)

    if(len(e[2].split('*'))==2):
        var[e[0]]=evalexp2(e[2],'*',var)

    return var



def evalexp2(e,v,var):
    """
    perform op in memory
    """

    e=e.split(v)
    a=int(var[e[0]])
    b=int(e[1])
    s=str(a)+v+str(b)
    return int(eval(s))        



def processaction(tr,var,D,M,x):
    """
    Perform individual action
    """

    cp=tr#for op
    tr=tr[0]#for r,w,o

    if(tr[0:4]=="READ"):
        #split
        tr=str_to_list(tr,"r")

        #bring to memory if not there
        if(tr[0] not in M):
            M[tr[0]]=D[tr[0]]
        
        #set val in var
        var[tr[1]]=M[tr[0]]


    elif(tr[0:5]=="WRITE"):
        #split
        tr=str_to_list(tr,"w")
        
        #add to log
        s="<"+x+", "+str(tr[0])+", "+str(M[tr[0]])+">"
        
        #change in memory
        M[tr[0]]=var[tr[1]]
        
        #printlog
        printlog(D,M,s)


    elif(tr[0:6]=="OUTPUT"):
        #split
        tr=str_to_list(tr,"o")

        #update in disk
        D[tr[0]]=M[tr[0]]
    

    else:
        var=evalexp(cp,var)


    return var,D,M



def runtr(D,T,M,X,start,var):
    """
    Run all transactions for X steps
    """

    #check if any trans can occur
    flag=False
    for x in T:
        if(len(T[x])>start):
            flag=True
            break
    
    #break if not
    if(flag==False):
        return flag,D,M,var

    #loop over all transactions
    for x in T:
        for y in range(start,min(start+X,len(T[x])),1):

            t=T[x][y]

            #check if tr starts
            if(y==0):
                s="<START "+x+">"
                printlog(D,M,s)
        
            #run transaction
            var,D,M=processaction(t,var,D,M,x)

            #check if tr ends
            if(y==len(T[x])-1):
                s="<COMMIT "+x+">"
                printlog(D,M,s)

    return flag,D,M,var



def printlog(D,M,s):
    """
    Print memory and log status in the given format
    """

    #print log
    print(s)

    #sort M and D
    Mt=sorted(M.keys())
    Dt=sorted(D.keys())

    #print M
    i=0
    for x in Mt:
        i+=1
        if(i==len(Mt)):
            print(x,M[x],end='')
        else:
            print(x,M[x],end=' ')
    print("")

    #print D
    i=0
    for x in Dt:
        i+=1
        if(i==len(Dt)):
            print(x,D[x],end='')
        else:
            print(x,D[x],end=' ')
    print("")



def processtr(D,T,X):
    """
    Run transactions in RR fashion
    """

    X=int(X)
    M={}
    start=0
    var={}

    #run until all transactions are over
    while(1):
        flag,D,M,var=runtr(D,T,M,X,start,var)
        if(flag==False):
            break
        else:
            start+=X



if __name__=="__main__":

    F=sys.argv[1]
    X=sys.argv[2]
    # print(F,X)
    Disk,Transactions=readinput(F)
    processtr(Disk,Transactions,X)