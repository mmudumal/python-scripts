import meminfoparameters as mfp
import pandas as pd

filename=raw_input('enter the meminfo filename:' )
mlist=mfp.parameters(filename)
g=globals()
mdict={}
for i in mlist:
    g[i]=[]
    with open(filename,'r') as sfile:
        for line in sfile.readlines():
            if line.startswith(i):
                g[i].append(line.split()[1])
        dict1={}
        dict1[i]=g[i]
        print i,len(g[i])
        mdict.update(dict1)
try:
    for k,v in mdict.iteritems():
        if len(v) !=30:
            del mdict[k]
except RuntimeError:
    print 'done'

df=pd.DataFrame(mdict)
print df.set_index('zz')
