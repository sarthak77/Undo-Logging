import sys

def readinput(file):
    """
    Returns contents of disk and transactions
    """

    Disk,Tran=[{},[]]
    
    with open(file,'r') as f:

        #read first line
        fl=f.readline()
        fl=fl.strip().split()

        for i in range(0,len(fl),2):
            Disk[fl[i]]=fl[i+1]

        # print(Disk)

        fl=f.readline()
        #read transactions
        for line in f:
            line=line.strip()
            line=line[1:-1]
            line=line.split()
            Tran.append(line)

        # for i in Tran:
        #     print(i)

    return [Disk,Tran]



def preprocess(T):
    """
    Convert T in a format easy to work
    """

    arr=["START","COMMIT","END"]

    for i in range(len(T)):
        tr=T[i]

        #update logs(remove ',')
        if(tr[0] not in arr):
            s=""
            s=s.join(tr)
            s=s.split(',')
            T[i]=s

        #start ckpts
        if(tr[1]=="CKPT"):

            #remove ()
            tr[2]=tr[2][1:]
            tr[-1]=tr[-1][:-1]

            #remove ','
            for j in range(2,len(tr),1):
                if(tr[j][-1]==","):
                    tr[j]=tr[j][:-1]

            T[i]=tr

    return T



def find_commit(T):
    """
    Return list of committed transactions
    """

    CT=[]
    for i in T:
        if(i[0]=="COMMIT"):
            CT.append(i[1])

    return CT



def remove_commit(T,CT):
    """
    Return updated transaction list after removing committed transactions
    """

    arr=["START","COMMIT","END","CKPT"]
    T_upd=[]
    for i in T:
        
        #start
        if(i[0]==arr[0]) and (i[1] not in CT) and(i[1] not in arr):
            T_upd.append(i)
        
        #update
        if(i[0] not in arr) and (i[0] not in CT):
            T_upd.append(i)

        #commit
        if(i[0]==arr[1]) and (i[1] not in CT):
            T_upd.append(i)
        
        #ckpt
        if(i[1]==arr[3]):
            temp=[]
            temp.append(i[0])
            temp.append(i[1])
            for j in range(2,len(i),1):
                if(i[j] not in CT):
                    temp.append(i[j])

            T_upd.append(temp)
                    
    return T_upd



def findckpt(T):
    """
    Return latest ckpt index
    """

    start=len(T)
    end=len(T)
    for i in range(len(T)):
        log=T[i]
        if(log[1]=="CKPT"):
            start=i
        if(log[0]=="END"):
            end=i
    
    start=len(T)-1-start
    end=len(T)-1-end

    return [start,end]



def get_end_index(T,start):
    """
    Return index till where we have to do recovery
    """

    last=start

    #find incomplete transactions
    incomplete=[]
    for i in range(2,len(T[start]),1):
        incomplete.append(T[start][i])


    for i in incomplete:
        for j in range(start,len(T),1):
            x=T[j]
            if(x[0]=="START" and x[1]==i):
                last=max(last,j)
                
    return last



def log_recovery(D,T):
    """
    Return recovered values in disk
    """

    #preprocessing
    T=preprocess(T)
    CT=find_commit(T)
    T=remove_commit(T,CT)
    start,end=findckpt(T)

    #reverse the list
    T.reverse()
    
    #initialise variables
    arr=["START","COMMIT","END"]
    last=len(T)

    #CASE-1 no start and no end
    if(start==-1 and end==-1):
        last=len(T)

    #CASE-2 no start but end (not possible)

    #CASE-3 start and no end
    elif(start!=-1 and end==-1):
        last=get_end_index(T,start)

    #CASE-3 start and end
    elif(start!=-1 and end!=-1):
        if(end<start):
            last=start
        else:
            last=get_end_index(T,start)

    #do recovery
    for i in range(last):
        tr=T[i]
        if(tr[0] not in arr):
            D[tr[1]]=tr[2]

    return D



def printdisk(D):
    """
    Print content of disk in the given format
    """

    Dt=sorted(D.keys())
    i=0
    for x in Dt:
        i+=1
        if(i==len(Dt)):
            print(x,D[x],end='')
        else:
            print(x,D[x],end=' ')
    print("")



if __name__=="__main__":

    F=sys.argv[1]
    # print(F,X)
    Disk,Transactions=readinput(F)
    Disk=log_recovery(Disk,Transactions)
    printdisk(Disk)