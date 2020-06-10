#here we summarize the read file functions, just put read optimal file and normal file together
import json
'''
number of nodes (switch)
number of edges (core)
number of demand pairs
average budgets #====TODO====what is this? seems flow entry limitation?

time elapsed during path selection
time elapsed during first step
time elapsed during first + second step

Z
total throuput before the second step
total throuput after the second step
number of path through each node  # for flow entries exp, to see which alg uses less flow entries on each node

number of path, total flow, and link utiliaztion of each edge # for failure exp, to see which alg has small failure impact on less paths
number of path and demand ratio of each st pair
# for failure exp, to see which alg has small failure impact on each st pair, this can use P(N > 30%) P(N > 50%) P(N > 70%) P(N > 90%) ...

Z, total throuput, and throuput ratio at single edge failure
# means the value of Z ... after each single edge failure, P(T > 90%) P(T > 95%) P(T > 99%) P(T > 99.9%) P(T > 99.9%)
# P(T > 90%) means for how many percent of failures, the throughput after failure are more than 90% of throughput before failrue

path set
paths selected
paths after the first step (minimize maximum link utilization)
paths after the second step (maximize total throuput)

'''

def readJSON(path):
    print path.split('/')[-1]
    file = open(path, "rb")
    fileJSON=json.load(file)
    return fileJSON

def readJSONLeband(path):
    file = open(path, "rb")
    fileJSON=json.load(file)
    print path.split('/')[-1]#.split('-')
    leband={}
    stpband={}
    for key in fileJSON:
        #print key
        if key=="Z":
            print key
            print fileJSON[key]
            #the optimal result of minimize max(le/ce) when input paths
        elif key=="total throuput before the second step":
            print key
            print fileJSON[key]
        elif key=="total throuput after the second step":
            #TODO what is the unit of this parameter, Mbps?
            print key
            print fileJSON[key]
        elif key=="number of path, total flow, and link utiliaztion of each edge":
            #print key
            #print fileJSON[key]
            temp=fileJSON[key]
            for e in temp:
                if e=='average':
                    #print e+' number of path, total flow, and link utiliaztion of each edge '+str(temp[e])
                    print e+' '+str(temp[e])
                    continue
                elist=str(e).split()
                #print elist
                leband[(elist[0],elist[1])]=temp[e][1]
        elif key=="paths after the second step (maximize total throuput)":
            #print key
            #print fileJSON[key]
            pathsband=fileJSON[key]
            for st in pathsband:
                sttemp=str(st).split()
                s=sttemp[0]
                t=sttemp[1]
                stpband[(s,t)]={}
                #print s,t,sttemp

                #print s,t
                for path in pathsband[st]:
                    if pathsband[st][path]>0:
                        stpband[(s,t)][str(path)]=pathsband[st][path]
                        #print path,stpband[(s,t)][str(path)]
    #print stpband
    print leband
    return leband
    #return fileJSON
