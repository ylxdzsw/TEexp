import json
#TODO compute l_e and max(le), lest[(i,j)][(s,t)]=value
#which means bandwidth allocation to s,t in edge (i,j) is equal to value

def readOptimal(path):
    print path.split('/')[-1]
    file = open(path, "rb")
    bandAllo=json.load(file)
    return bandAllo


def readOptimalLeband(path):
    print path.split('/')[-1]
    lest={}#lest[(i,j)][(s,t)]=band
    le={}#le[(i,j)]=[band1,band2,...]
    leband={}#le[(i,j)]=bandsum
    steband={}
    file = open(path, "rb")
    bandAllo=json.load(file)
    for key in bandAllo:
        #print key
        #print bandAllo[key]
        if key=='Z':
            print 'Optimal min(max(le/ce)) =',bandAllo[key]
            continue
        tempkey=str(key).split()
        i=tempkey[2]
        j=tempkey[3]
        s=tempkey[0]
        t=tempkey[1]
        band=bandAllo[key]
        if (s,t) not in steband:
            steband[(s,t)]={}
        if (i,j) not in le:
            lest[(i,j)]={}
            le[(i,j)]=[]
        if band<>0:
            le[(i,j)].append(band)
            lest[(i,j)][(s,t)]=band
            steband[(s,t)][(i,j)]=band
    minmaxle=0
    for key in le:
        sumle=sum(le[key])
        leband[key]=sumle
        if minmaxle<sumle:
            minmaxle=sumle
    print minmaxle
    #print le
    #print lest
    """
    for (s,t) in steband:
        print s,t
        for (i,j) in steband[(s,t)]:
            print str(i)+'->'+str(j),steband[(s,t)][(i,j)]
        #print steband[(s,t)]
    """
    print '\n'
    print leband
    print 'optimal end\n'
    return leband
    #return fileOptimal#TODO TODO we may add a new function to compute leband etc.
