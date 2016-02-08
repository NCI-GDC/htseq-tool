import scipy as sp
import sys

def getLength(fn_anno):
    ''' 
    input gtf annotation and output all exonic positions
    '''

    anno  = sp.loadtxt(fn_anno, delimiter = '\t', dtype = 'string', usecols=[2,3,4,8])
    chrm  = sp.loadtxt(fn_anno, delimiter = '\t', dtype = 'string', usecols=[0])
    anno  = anno[anno[:,0] == 'exon',:] ### filter down to exons
    pos   = anno[:,1:3].astype('int')
    
    gid   = [x.split(';')[0] for x in anno[:,3]] ### clean gene id's
    gid   = sp.array([x.split(" ")[1].strip('\"') for x in gid])
    
    ugid  = sp.unique(gid)
    gnL   = sp.zeros(ugid.shape[0])
    for i,mgid in enumerate(ugid):
        if (i % 100) == 0:
            sys.stdout.write("%i out of %i \n" % (i, ugid.shape[0]))
        mpos   = sp.hstack([range(x[0],x[1]+1) for x in pos[mgid == gid,:]]) ### positions for this frame
        gnL[i] = sp.unique(mpos).shape[0]
    return ugid, gnL
