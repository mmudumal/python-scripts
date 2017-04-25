def parameters(memfile):
    tlist=[]
    mlist=[]
    with open(memfile,'r') as sfile:
        for line in sfile.readlines():
            member=line.split()[0][0:-1]
            tlist.append(member)
        mlist=list(set(tlist))
        return mlist
