#summarize we want which kind of figures
#1. Z<=1 the performance ratio, 2. Z>1 the throughput ratio
#3. the performance increase for each alg?
#compare the whole throughput between step 1: min(max(le)) with step 2: maximize whole network throughput ?
#4. path utilization CDF
#5. flow entries CCDF
#6. link utilizations CDF for alg comparison, and for step 1, step 2, optimal comparison (like for Custom)
#7. fairness: each s-t satisfied how many demands
#8. robustness: after single link failure, data plane reacting (TODO can satisfy how many rerouting traffic and loss how many)
#after single link failure, control plane reacting: throughput after recomputing TE
#9. computing time
#10. latency (path length or better use gscale testbed to get the real data TODO)
#11. reacting to TM changes? or path updating or?

from readJSON import readJSON, readJSONLeband
from readOptimal import readOptimal, readOptimalLeband
from drawFigures import drawFigure, drawBenefit
from CDF import cdf, ccdf, drawCDFandCCDF
from numpy import *

def analysisZ(demands, pathpre, topo, algdic, comp, figurepath):#compare): #for #1 and #2
    Zless1={}
    Zlarge1={}

    for d in demands:
        #Zless1[d]={}
        #Zlarge1[d]={}
        filename=pathpre+topo+"-"+str(d)+"-optimal-mcf.json"
        #Z,leband=readOptimal(filename)#TODO here need to be consistant for each anamethods
        fileOptimal=readOptimal(filename)
        Z=fileOptimal['Z']
        if Z<=1:#fileOptimal['Z']<=1:
            Zless1[d]={}
            Zless1[d]['Optimal']=Z#fileOptimal['Z']
        elif Z<2.5:
            Zlarge1[d]={}
            Zlarge1[d]['Optimal']=Z#fileOptimal['Z']
        print "============"

    for d in Zless1:#demands:
        for alg in algdic:
            #for comp in compare:
            filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
            fileJSON=readJSON(filename)
            Zless1[d][alg]=fileJSON['Z']
    #TODO first get the result for hardnop
            print "============"

    for d in Zlarge1:
        for alg in algdic:
            #for comp in compare:
            filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
            fileJSON=readJSON(filename)
            Zlarge1[d][alg]=[]
            Zlarge1[d][alg].append(fileJSON['Z'])#Save also throughput before second step and after second step
            Zlarge1[d][alg].append(fileJSON['total throuput before the second step'])
            Zlarge1[d][alg].append(fileJSON['total throuput after the second step'])
            #TODO first get the result for hardnop
            print "============"


    print Zless1
    print Zlarge1

    #drawBenefit(Zless1,1,4,'Z','Performance ratio (Zalg/Zopt)','Z-gscale-1-hardnop-Zless1.pdf')
    drawBenefit(Zless1,1,6,'Z','Performance ratio (Zalg/Zopt)','Z-'+topo+'-1-'+comp+'-Zless1all.pdf', figurepath)

    drawBenefit(Zlarge1,0,6,'Z','Throughput ratio (Talg/(sum(TM)/Zopt))','Z-'+topo+'-1-'+comp+'-Zlarge1-TZall.pdf', figurepath)
    #TODO here we need to make clear why we can not call the drawBenefit at the same twice
    return Zless1, Zlarge1#TODO test it

def analysisAlgT(demands, pathpre, topo, alg, figurepath): #for #3
    Zprogram= [] #TODO or demand?
    bandallostep1 = []# Smore: use only minimize the maximum link utilization
    bandallostep2 = []

    Zhardnop= []
    hardbandallostep1 = []
    hardbandallostep2 = []
    for d in demands:
        filename=pathpre+topo+"-"+str(d)+"-"+alg+"-program.json"
        #[Z,Tstep1,Tstep2]=readJSON(filename)
        fileJSON=readJSON(filename)#TODO here we need to get the value we want
        Z=fileJSON['Z']
        Tstep1=fileJSON['total throuput before the second step']
        Tstep2=fileJSON['total throuput after the second step']
        Zprogram.append(Z)
        bandallostep1.append(Tstep1)
        bandallostep2.append(Tstep2)
    #for d in demands:
        filename=pathpre+topo+"-"+str(d)+"-"+alg+"-hardnop.json"
        #[Z,Tstep1,Tstep2]=readJSON(filename)#TODO here we need to get the value we want

        Z=fileJSON['Z']
        Tstep1=fileJSON['total throuput before the second step']
        Tstep2=fileJSON['total throuput after the second step']

        Zhardnop.append(Z)
        hardbandallostep1.append(Tstep1)
        hardbandallostep2.append(Tstep2)
    figname=topo+"-"+alg+"-program-hardnop.pdf"
    drawFigure(Zprogram, bandallostep1, bandallostep2, Zhardnop, hardbandallostep1, hardbandallostep2, figname, figurepath)

def analysisPaths(Zless1, demands, pathpre, topo, algdic, compare, figurepath):
#TODO TODO add ? path analysis for Zlarge1?
    if len(Zless1)==0:
        Zless1={}
        Zlarge1={}
        for d in demands:
            filename=pathpre+topo+"-"+str(d)+"-optimal-mcf.json"
            #Z,leband,lest,steband=readOptimal(filename)
            fileOptimal=readOptimal(filename)
            Z=fileOptimal['Z']
            if Z<=1:#fileOptimal['Z']<=1:
                Zless1[d]={}
                Zless1[d]['Optimal']=Z#fileOptimal['Z']
            elif Z<2.5:
                Zlarge1[d]={}
                Zlarge1[d]['Optimal']=Z#fileOptimal['Z']
                print "============"

    ndzles = len(Zless1)

    algPathSet={}
    stpUtilize={}#This can be initialized only once then record the path utilization for each TM
    #   { alg : { stpair : { path1 : %x, path2: %y, ...}}}
    #or { alg : { stpair : { path1 : [%x, di,...] , path2 : [%y, dj,...], ...} ... } ... }
    for d in Zless1:#demands:
        #TODO analysis path utilization and when Z<1 we can some how find the relationship
        #between optimal link using for each s-t pair compared with other algs
        for alg in algdic:
            if alg not in stpUtilize:
                algPathSet[alg]={}
                stpUtilize[alg]={}
            for comp in compare:#here actually includes only one method like ["hardnop"]
                filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
                fileJSON=readJSON(filename)
                Zless1[d][alg]=fileJSON['Z']

                key = "paths after the second step (maximize total throuput)"
            #TODO analysis the path utilization
            #for i in 1:n, j in 1:n @when i != j
            #    demand["$(hosts[i]) $(hosts[j])"] = line[(i-1) * n + j] / 2^20 # to Megabyte
                stpband={}
                #print key
                #print fileJSON[key]
                pathsband=fileJSON[key]
                #print pathsband
                leband={}

                for st in pathsband:

                    sttemp=str(st).split()
                    s=sttemp[0]
                    t=sttemp[1]
                    stpband[(s,t)]={}
                    #print s,t,sttemp

                    #print s,t
                    sv=int(s[1:])#TODO for gscale we can do like this but for Cernet we need to read hosts
                    tv=int(t[1:])
                    if (s,t) not in stpUtilize[alg]:
                        stpUtilize[alg][(s,t)]={}

                    for path in pathsband[st]:
                        #TODO at least for ksp each time the path set is the same
                        if str(path) not in stpUtilize[alg][(s,t)]:
                            algPathSet[alg][str(path)]=0
                            stpUtilize[alg][(s,t)][str(path)]=[0]

                        if pathsband[st][path]>0:

                            stpUtilize[alg][(s,t)][str(path)][0]+=1*1.0/ndzles
                            stpUtilize[alg][(s,t)][str(path)].append(d)

                            algPathSet[alg][str(path)]+=1*1.0/ndzles

                            stpband[(s,t)][str(path)]=pathsband[st][path]
                            ptemp = str(path).split("->")
                            del ptemp[0]
                            del ptemp[-1]
                            ilen=len(ptemp)-1
                            for i in range(ilen):
                                if (ptemp[i],ptemp[i+1]) not in leband:
                                    leband[(ptemp[i],ptemp[i+1])]=0
                                #TODO cal or get demand for corresponding topo and d (JSON file)
                                #leband[(ptemp[i],ptemp[i+1])]+=pathsband[st][path]*demand49gscale[(sv-1)*12+tv-1]*1.0/pow(2,20)/1000#here need to *demand(s,t)
                #print 'Step 2',stpband,leband#TODO not right
                #first get the result for hardnop
                print "============"

    print 'Zless1',Zless1,len(Zless1)
    print 'stpUtilize',stpUtilize

    dictx={}
    dicty={}

    for alg in algdic:
        data=[algPathSet[alg][key] for key in algPathSet[alg]]
        #x,y=ccdf(data)
        x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zless1-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,1,'Path utilization','Path-'+topo+'-1-Zless1-'+comp+'-cdf.pdf',figurepath)

def analysisFlowEntries(d, pathpre, topo, algdic, comp, figurepath):

    dictx={}
    dicty={}
    for alg in algdic:
        #for comp in compare:
        filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
        fileJSON=readJSON(filename)

        key="number of path through each node"
        #compute the y=p(X>x)
        data=[]
        temp=fileJSON[key]
        for e in temp:
            if e=='average':
                print e+' '+str(temp[e])
                continue
            else:
                data.append(temp[e])
        print data
        x,y=ccdf(data)
        dictx[alg]=x
        dicty[alg]=y
        print "============"
    #drawCDFandCCDF(dictx,dicty,2,0,'# flow entries','flow-gscale-1-'+comp+'-ccdf.pdf',figurepath)
    drawCDFandCCDF(dictx,dicty,6,0,'# flow entries','flow-'+topo+'-1-'+comp+'-ccdf.pdf',figurepath)

def analysisLinksU(d, hostsdemand, pathpre, topo, algdic, comp, figurepath):

    dictx={}
    dicty={}
    #demand49gscale=[2.2578562426522303e8... #TODO TODO This can still be used as our demand is not change for gscale, Cernet,
    # but more precise way is to use a function to get he corrsponding demand line
    leband={}
    for alg in algdic:#here is 'Custom' only for this function
        #for comp in compare:
        filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
        fileJSON=readJSON(filename)


        key="number of path, total flow, and link utiliaztion of each edge"
        #print key
        #print fileJSON[key]
        data=[]
        temp=fileJSON[key]
        for e in temp:
            if e=='average':
                #print e+' number of path, total flow, and link utiliaztion of each edge '+str(temp[e])
                print e+' '+str(temp[e])
                continue
            else:
                data.append(temp[e][1]*1.0/1000)
            #elist=str(e).split()
            #print elist
            #leband[(elist[0],elist[1])]=temp[e][1]

        # key="number of path through each node"
        # #compute the y=p(X>=x)
        # data=[]
        # temp=fileJSON[key]
        # for e in temp:
        #     if e=='average':
        #         print e+' '+str(temp[e])
        #         continue
        #     else:
        #         data.append(temp[e])
        print data
        #x,y=ccdf(data)
        x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y
        print "============"

        #if alg<>"Custom":#TODO TODO here only analysis Custom
        #    continue#TODO here we use our custom (maximum number of edge disjoint paths) to compute the TM/Z
        key='Z'
        Z=fileJSON[key]
        key="paths after the first step (minimize maximum link utilization)"

    #for i in 1:n, j in 1:n @when i != j
    #    demand["$(hosts[i]) $(hosts[j])"] = line[(i-1) * n + j] / 2^20 # to Megabyte


        stpband={}
        #print key
        #print fileJSON[key]
        pathsband=fileJSON[key]
        #print pathsband
        leband={}
        for st in pathsband:
            sttemp=str(st).split()
            s=sttemp[0]
            t=sttemp[1]
            stpband[(s,t)]={}
            #print s,t,sttemp

            #print s,t
            sv=int(s[1:])
            tv=int(t[1:])
            for path in pathsband[st]:
                if pathsband[st][path]>0:
                    stpband[(s,t)][str(path)]=pathsband[st][path]
                    ptemp = str(path).split("->")
                    del ptemp[0]
                    del ptemp[-1]
                    ilen=len(ptemp)-1
                    for i in range(ilen):
                        if (ptemp[i],ptemp[i+1]) not in leband:
                            leband[(ptemp[i],ptemp[i+1])]=0
                        leband[(ptemp[i],ptemp[i+1])]+=pathsband[st][path]*hostsdemand[str(st)]*1.0/pow(2,20)/1000#demandd[(sv-1)*12+tv-1]*1.0/pow(2,20)/1000#demand49gscale[(sv-1)*12+tv-1]*1.0/pow(2,20)/1000#here need to *demand(s,t)
        print 'TM/Z',stpband,leband#TODO here for Cernet need to change

    data=[leband[key] for key in leband]
    x,y=cdf(data)
    #dictx['TM (Custom)']=x
    #dicty['TM (Custom)']=y

    dictx['TM ('+alg+')']=x#TODO test this one
    dicty['TM ('+alg+')']=y


    data=[leband[key]*1.0/Z for key in leband]
    x,y=cdf(data)
    #dictx['TM/Z (Custom)']=x
    #dicty['TM/Z (Custom)']=y

    dictx['TM/Z ('+alg+')']=x
    dicty['TM/Z ('+alg+')']=y

    filename=pathpre+topo+"-"+str(d)+"-optimal-mcf.json"
    #leband=readOptimal(filename)#TODO calculate here?
    leband=readOptimalLeband(filename)
    data=[leband[key]*1.0/1000 for key in leband]
    print 'optimal',data
    x,y=cdf(data)
    dictx['Minimize(max(le))']=x
    dicty['Minimize(max(le))']=y
    #dictx['Optimal']=x
    #dicty['Optimal']=y

    #drawCDFandCCDF(dictx,dicty,2,0,'link utilization','le-gscale-1-hardnop-ccdfd50.pdf')
    #drawCDFandCCDF(dictx,dicty,2,1,'link utilization','le-gscale-1-hardnop-cdftest40.pdf')
    #drawCDFandCCDF(dictx,dicty,2,1,'link utilization','le-gscale-1-program-cdftest30.pdf')
    drawCDFandCCDF(dictx,dicty,4,1,'link utilization','le-'+topo+'-1-'+alg+'-'+comp+'-cdfcomp1algTMZstep1-d'+str(d)+'.pdf',figurepath)

def analysisAlgsLinksU(d, pathpre, topo, algdic, comp, figurepath):

    dictx={}
    dicty={}
    for alg in algdic:
        #for comp in compare:
        filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
        fileJSON=readJSON(filename)


        key="number of path, total flow, and link utiliaztion of each edge"
        #print key
        #print fileJSON[key]
        data=[]
        temp=fileJSON[key]
        for e in temp:
            if e=='average':
                #print e+' number of path, total flow, and link utiliaztion of each edge '+str(temp[e])
                print e+' '+str(temp[e])
                continue
            else:
                data.append(temp[e][1]*1.0/1000)
        print data
        #x,y=ccdf(data)
        x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y
        print "============"
    #drawCDFandCCDF(dictx,dicty,2,0,'link utilization','le-gscale-1-hardnop-ccdfd50.pdf')
    drawCDFandCCDF(dictx,dicty,6,1,'link utilization','le-'+topo+'-1-'+comp+'-cdfalld'+str(d)+'.pdf', figurepath)

def analysisPathlength(Zless1, demands, pathpre, topo, algdic, compare, figurepath):
#TODO here Zless1 actually can stands for a lot of things?
#TODO TODO consider for Z<=1 only or any Z?,
#the difference is that for Z>1 the total throughput of each alg after step 2 may not be the same
#TODO each s-t first get the average path length?, then draw CCDF for each alg (for all the s-t pairs)
    if len(Zless1)==0:
        Zless1={}
        Zlarge1={}
        for d in demands:
            filename=pathpre+topo+"-"+str(d)+"-optimal-mcf.json"
            #Z,leband,lest,steband=readOptimal(filename)
            fileOptimal=readOptimal(filename)
            Z=fileOptimal['Z']
            if Z<=1:#fileOptimal['Z']<=1:
                Zless1[d]={}
                Zless1[d]['Optimal']=Z#fileOptimal['Z']
            elif Z<2.5:
                Zlarge1[d]={}
                Zlarge1[d]['Optimal']=Z#fileOptimal['Z']
                print "============"

    ndzles = len(Zless1)

    algPathSet={}
    stpUtilize={}#This can be initialized only once then record the path utilization for each TM
    #   { alg : { stpair : { path1 : %x, path2: %y, ...}}}
    #or { alg : { stpair : { path1 : [%x, di,...] , path2 : [%y, dj,...], ...} ... } ... }
    algstpathlen={}
    for d in Zless1:#demands:
        #TODO analysis path utilization and when Z<1 we can some how find the relationship
        #between optimal link using for each s-t pair compared with other algs
        for alg in algdic:
            if alg not in stpUtilize:
                algPathSet[alg]={}
                stpUtilize[alg]={}
                algstpathlen[alg]={}
            for comp in compare:#here actually includes only one method like ["hardnop"]
                filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
                fileJSON=readJSON(filename)
                Zless1[d][alg]=fileJSON['Z']
                key = "paths after the second step (maximize total throuput)"
                stpband={}
                pathsband=fileJSON[key]
                leband={}
                for st in pathsband:
                    sttemp=str(st).split()
                    s=sttemp[0]
                    t=sttemp[1]
                    stpband[(s,t)]={}
                    sv=int(s[1:])#TODO for gscale we can do like this but for Cernet we need to read hosts
                    tv=int(t[1:])
                    plentemp=0
                    pntemp=0
                    if (s,t) not in stpUtilize[alg]:
                        stpUtilize[alg][(s,t)]={}
                        algstpathlen[alg][(s,t)]=[0,0,100,0]
                        #first average path length, second average path number?, min len, max len?
                    for path in pathsband[st]:
                        #TODO at least for ksp each time the path set is the same
                        if str(path) not in stpUtilize[alg][(s,t)]:
                            algPathSet[alg][str(path)]=0
                            stpUtilize[alg][(s,t)][str(path)]=[0]
                        if pathsband[st][path]>0:
                            pntemp+=1
                            stpUtilize[alg][(s,t)][str(path)][0]+=1*1.0/ndzles
                            stpUtilize[alg][(s,t)][str(path)].append(d)

                            algPathSet[alg][str(path)]+=1*1.0/ndzles

                            stpband[(s,t)][str(path)]=pathsband[st][path]
                            ptemp = str(path).split("->")

                            plentemp+=len(ptemp)-1
                            if len(ptemp)-1<algstpathlen[alg][(s,t)][2]:
                                algstpathlen[alg][(s,t)][2]=len(ptemp)-1
                            if len(ptemp)-1>algstpathlen[alg][(s,t)][3]:
                                algstpathlen[alg][(s,t)][3]=len(ptemp)-1

                            del ptemp[0]
                            del ptemp[-1]
                            ilen=len(ptemp)-1
                            for i in range(ilen):
                                if (ptemp[i],ptemp[i+1]) not in leband:
                                    leband[(ptemp[i],ptemp[i+1])]=0
                    #print plentemp,pntemp,algstpathlen[alg][(s,t)][0]
                    algstpathlen[alg][(s,t)][0]=algstpathlen[alg][(s,t)][0]+plentemp*1.0/pntemp/1.0/ndzles
                    algstpathlen[alg][(s,t)][1]=algstpathlen[alg][(s,t)][1]+pntemp/1.0/ndzles

                #algstpathlen[alg][(s,t)][0]=algstpathlen[alg][(s,t)][0]/1.0/ndzles
                #algstpathlen[alg][(s,t)][1]=algstpathlen[alg][(s,t)][1]/1.0/ndzles

                                #TODO cal or get demand for corresponding topo and d (JSON file)
                                #leband[(ptemp[i],ptemp[i+1])]+=pathsband[st][path]*demand49gscale[(sv-1)*12+tv-1]*1.0/pow(2,20)/1000#here need to *demand(s,t)
                #print 'Step 2',stpband,leband#TODO not right
                #first get the result for hardnop
                #print "============"

    print 'Zless1',Zless1,len(Zless1)
    #print 'stpUtilize',stpUtilize
    print 'algstpathlen ',algstpathlen
    dictx={}
    dicty={}

    for alg in algdic:
        data=[algstpathlen[alg][key][0] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zless1-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Average path length of each s-t pair','Pathlength-'+topo+'-1-Zless1-'+comp+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][1] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zless1-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'# used path of each s-t pair','Pathnum-'+topo+'-1-Zless1-'+comp+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][3] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zless1-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Length of the longest used s-t path','Pathmaxlen-'+topo+'-1-Zless1-'+comp+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][3] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zless1-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Length of the shortest used s-t path','Pathmaxlen-'+topo+'-1-Zless1-'+comp+'-ccdf.pdf',figurepath)

def analysisPathlength1(Zrelated, lessorlargeorall, demands, pathpre, topo, algdic, compare, figurepath):
#TODO here Zrelated actually can stands for a lot of things?
#TODO TODO consider for Z<=1 only or any Z?,
#the difference is that for Z>1 the total throughput of each alg after step 2 may not be the same
#TODO each s-t first get the average path length?, then draw CCDF for each alg (for all the s-t pairs)
    Zinname=''
    if len(Zrelated)==0:
        Zless1={}
        Zlarge1={}
        for d in demands:
            filename=pathpre+topo+"-"+str(d)+"-optimal-mcf.json"
            #Z,leband,lest,steband=readOptimal(filename)
            fileOptimal=readOptimal(filename)
            Z=fileOptimal['Z']
            if Z<=1:#fileOptimal['Z']<=1:
                Zless1[d]={}
                Zless1[d]['Optimal']=Z#fileOptimal['Z']
            elif Z<2.5:
                Zlarge1[d]={}
                Zlarge1[d]['Optimal']=Z#fileOptimal['Z']
                print "============"
        if lessorlargeorall==3:
            Zrelated=demands
            Zinname='all'
        elif lessorlargeorall==2:
            Zrelated=Zless1
            Zinname='Zlarge1'
        elif lessorlargeorall==1:
            Zrelated=Zlarge1
            Zinname='Zless1new'
    else:
        if lessorlargeorall==3:
            Zinname='all'
        elif lessorlargeorall==2:
            Zinname='Zlarge1'
        elif lessorlargeorall==1:
            Zinname='Zless1new'
    ndzles = len(Zrelated)

    algPathSet={}
    stpUtilize={}#This can be initialized only once then record the path utilization for each TM
    #   { alg : { stpair : { path1 : %x, path2: %y, ...}}}
    #or { alg : { stpair : { path1 : [%x, di,...] , path2 : [%y, dj,...], ...} ... } ... }
    algstpathlen={}
    for d in Zrelated:#demands:
        #TODO analysis path utilization and when Z<1 we can some how find the relationship
        #between optimal link using for each s-t pair compared with other algs
        for alg in algdic:
            if alg not in stpUtilize:
                algPathSet[alg]={}
                stpUtilize[alg]={}
                algstpathlen[alg]={}
            for comp in compare:#here actually includes only one method like ["hardnop"]
                filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
                fileJSON=readJSON(filename)
                #Zrelated[d][alg]=fileJSON['Z']
                key = "paths after the second step (maximize total throuput)"
                stpband={}
                pathsband=fileJSON[key]
                leband={}
                for st in pathsband:
                    sttemp=str(st).split()
                    s=sttemp[0]
                    t=sttemp[1]
                    stpband[(s,t)]={}
                    sv=int(s[1:])#TODO for gscale we can do like this but for Cernet we need to read hosts
                    tv=int(t[1:])
                    plentemp=0
                    pntemp=0
                    if (s,t) not in stpUtilize[alg]:
                        stpUtilize[alg][(s,t)]={}
                        algstpathlen[alg][(s,t)]=[0,0,100,0]
                        #first average path length, second average path number?, min len, max len?
                    for path in pathsband[st]:
                        #TODO at least for ksp each time the path set is the same
                        if str(path) not in stpUtilize[alg][(s,t)]:
                            algPathSet[alg][str(path)]=0
                            stpUtilize[alg][(s,t)][str(path)]=[0]
                        if pathsband[st][path]>0:
                            pntemp+=1
                            stpUtilize[alg][(s,t)][str(path)][0]+=1*1.0/ndzles
                            stpUtilize[alg][(s,t)][str(path)].append(d)

                            algPathSet[alg][str(path)]+=1*1.0/ndzles

                            stpband[(s,t)][str(path)]=pathsband[st][path]
                            ptemp = str(path).split("->")

                            plentemp+=len(ptemp)-1
                            if len(ptemp)-1<algstpathlen[alg][(s,t)][2]:
                                algstpathlen[alg][(s,t)][2]=len(ptemp)-1
                            if len(ptemp)-1>algstpathlen[alg][(s,t)][3]:
                                algstpathlen[alg][(s,t)][3]=len(ptemp)-1

                            del ptemp[0]
                            del ptemp[-1]
                            ilen=len(ptemp)-1
                            for i in range(ilen):
                                if (ptemp[i],ptemp[i+1]) not in leband:
                                    leband[(ptemp[i],ptemp[i+1])]=0
                    #print plentemp,pntemp,algstpathlen[alg][(s,t)][0]
                    algstpathlen[alg][(s,t)][0]=algstpathlen[alg][(s,t)][0]+plentemp*1.0/pntemp/1.0/ndzles
                    algstpathlen[alg][(s,t)][1]=algstpathlen[alg][(s,t)][1]+pntemp/1.0/ndzles

                #algstpathlen[alg][(s,t)][0]=algstpathlen[alg][(s,t)][0]/1.0/ndzles
                #algstpathlen[alg][(s,t)][1]=algstpathlen[alg][(s,t)][1]/1.0/ndzles

                                #TODO cal or get demand for corresponding topo and d (JSON file)
                                #leband[(ptemp[i],ptemp[i+1])]+=pathsband[st][path]*demand49gscale[(sv-1)*12+tv-1]*1.0/pow(2,20)/1000#here need to *demand(s,t)
                #print 'Step 2',stpband,leband#TODO not right
                #first get the result for hardnop
                #print "============"

    #print 'Zrelated',Zrelated,len(Zrelated)
    #print 'stpUtilize',stpUtilize
    #print 'algstpathlen ',algstpathlen
    dictx={}
    dicty={}

    for alg in algdic:
        data=[algstpathlen[alg][key][0] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zrelated-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Average path length of each s-t pair','Pathlength-'+topo+'-1-'+Zinname+'-'+comp+str(len(compare))+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][1] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zrelated-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'# used path of each s-t pair','Pathnum-'+topo+'-1-'+Zinname+'-'+comp+str(len(compare))+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][3] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zrelated-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Length of the longest used s-t path','Pathmaxlen-'+topo+'-1-'+Zinname+'-'+comp+str(len(compare))+'-ccdf.pdf',figurepath)

    for alg in algdic:
        data=[algstpathlen[alg][key][2] for key in algstpathlen[alg]]
        x,y=ccdf(data)#y=P(X>x)
        #x,y=cdf(data)
        dictx[alg]=x
        dicty[alg]=y

    #drawCDFandCCDF(dictx,dicty,2,0,'Path utilization','Path-gscale-1-Zrelated-ccdf.pdf')
    drawCDFandCCDF(dictx,dicty,6,0,'Length of the shortest used s-t path','Pathminlen-'+topo+'-1-'+Zinname+'-'+comp+str(len(compare))+'-ccdf.pdf',figurepath)

#1. fairness: get the average? satisfied demand ratio (%) for each s-t pair, consider whether include Zopt<=1(will mostly be 1) , Z>1
#2. robustness: as we have shown that each s-t almost all use 1 path only (only one path has weight)
#therefore, we are hard to reroute in data plane use the normalized weight (TODO or just send packet out using equal weight to each healthy tunnel), ? TODO,
#2.1 get the percent that how many single link failure lead to some s-t pair unreachable
#2.2 get the Histogram of P(T>95%), P(T>95%), P(T>95%), P(T>95%), P(T>95%)
#2.3 get the throughput ratio CDF
def fairness(Zrelated, lessorlargeorall, pathpre, topo, algdic, comp, figurepath):
    if lessorlargeorall==3:
        Zinname='all'
    elif lessorlargeorall==2:
        Zinname='Zlarge1'
    elif lessorlargeorall==1:
        Zinname='Zless1'


    dictx={}
    dicty={}
    algstdratio={}
    algstdratioH={}
    for alg in algdic:
        #if alg not in algstdratio:
        #    algstdratio[alg]=[]
        alldsumtemp=[]#mat([])
        for d in Zrelated:
        #for comp in compare:
            filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
            fileJSON=readJSON(filename)

            key="number of path and demand ratio of each st pair"
            #    "h22 h17": [3.0,46.54156150185264],
            #compute the y=p(X>x)
            data=[]
            temp=fileJSON[key]
            if 'average' in temp:
                del temp['average']
            if len(alldsumtemp)==0:
                alldsumtemp=mat([0]*len(temp))
            data=[float(temp[st][1]) for st in sorted(temp)]
            data=mat(data)
            alldsumtemp=alldsumtemp+data
            #print alldsumtemp
        #print alldsumtemp
        alldsumtemp=alldsumtemp*1.0/100/len(Zrelated)
        algstdratio[alg]=alldsumtemp.tolist()[0]
        print algstdratio[alg]
        x,y=ccdf(algstdratio[alg])
        dictx[alg]=x
        dicty[alg]=y
        #keylist=["P(T > 90%)","P(T > 95%)","P(T > 99%)","P(T > 99.9%)","P(T > 99.99%)"]
        percy=[0,0,0,0,0]

        for i in range(len(x)):
            percx=x[i]
            if percy[0]==0 and percx>=0.9:
                if percx==0.9 or i==0:
                    percy[0]=y[i]
                else:
                    percy[0]=y[i-1]
            elif percy[1]==0 and percx>=0.95:
                if percx==0.95 or i==0:
                    percy[1]=y[i]
                else:
                    percy[1]=y[i-1]
            elif percy[2]==0 and percx>=0.99:
                if percx==0.99 or i==0:
                    percy[2]=y[i]
                else:
                    percy[2]=y[i-1]
            elif percy[3]==0 and percx>=0.999:
                if percx==0.999 or i==0:
                    percy[3]=y[i]
                else:
                    percy[3]=y[i-1]
            elif percy[4]==0 and percx>=0.9999:
                if percx==0.9999 or i==0:
                    percy[4]=y[i]
                else:
                    percy[4]=y[i-1]
        #print percy
        #print "============"
        algstdratioH[alg]=percy
    #print algstdratio
    print algstdratioH
    #drawCDFandCCDF(dictx,dicty,2,0,'# flow entries','flow-gscale-1-'+comp+'-ccdf.pdf',figurepath)
    drawCDFandCCDF(dictx,dicty,6,0,'Satisfied demand ratio of each s-t pair','dratio-'+topo+'-1-'+Zinname+'-'+comp+'-ccdf.pdf',figurepath)
    #TODO draw Histogram for "P(T > 95%)","P(T > 90%)","P(T > 99%)","P(T > 99.9%)","P(T > 99.99%)"
def robustness(Zrelated, lessorlargeorall, pathpre, topo, algdic, comp, figurepath):
    #key="Z, total throuput, and throuput ratio at single edge failure"
    if lessorlargeorall==3:
        Zinname='all'
    elif lessorlargeorall==2:
        Zinname='Zlarge1'
    elif lessorlargeorall==1:
        Zinname='Zless1'

    keylist=["P(T > 90%)","P(T > 95%)","P(T > 99%)","P(T > 99.9%)","P(T > 99.99%)"]

    dictx={}
    dicty={}
    #algetratio={}
    algetratioH={}
    algefailunreach={}
    for alg in algdic:
        #if alg not in algstdratio:
        #    algstdratio[alg]=[]
        alldsumtemp=[]#mat([])
        alldsumH=[]
        dunreachtemp=[]
        for d in Zrelated:
        #for comp in compare:
            filename=pathpre+topo+"-"+str(d)+"-"+alg+"-"+comp+".json"
            fileJSON=readJSON(filename)

            key="Z, total throuput, and throuput ratio at single edge failure"
            #"s6 s7": [3.1532651852755422, 14672.0837296913, 91.61506879097249],
            #compute the y=p(X>x)
            data=[]
            dataH=[]
            unreachN=0
            temp=fileJSON[key]
            if 'average' in temp:
                del temp['average']
            if len(alldsumH)==0:
                alldsumH=mat([0]*len(keylist))
            for prob in keylist:
                dataH.append(temp[prob])
                del temp[prob]

            dataH=mat(dataH)
            alldsumH=alldsumH+dataH

            # TODO this can not use mat to add all , as some link down may lead to "some pairs have no path"
            for k in temp:
                if temp[k]=="some pairs have no path":
                    unreachN=unreachN+1
            dunreachtemp.append(unreachN)
            if len(alldsumtemp)==0:
                alldsumtemp=mat([0]*len(temp))


            #data=[float(temp[e][2]) for e in sorted(temp)]
            #data=mat(data)
            #alldsumtemp=alldsumtemp+data
            #print alldsumtemp
        #print alldsumtemp
        alldsumH=alldsumH*1.0/len(Zrelated)#remember it is % is OK
        algetratioH[alg]=alldsumH.tolist()[0]
        #alldsumtemp=alldsumtemp*1.0/100/len(Zrelated)
        #algetratio[alg]=alldsumtemp.tolist()[0]
        #print algetratio[alg]
        algefailunreach[alg]=dunreachtemp
        #x,y=ccdf(algetratio[alg])
        x,y=ccdf(algefailunreach[alg])
        dictx[alg]=x
        dicty[alg]=y
        print "============"
    print algetratioH
    print algefailunreach
    #print algstdratio
    #drawCDFandCCDF(dictx,dicty,2,0,'# flow entries','flow-gscale-1-'+comp+'-ccdf.pdf',figurepath)
    #drawCDFandCCDF(dictx,dicty,6,0,'Satisfied whole throughput ratio','tratio-'+topo+'-1-'+Zinname+'-'+comp+'-ccdf.pdf',figurepath)
    #drawCDFandCCDF(dictx,dicty,6,0,'Percent of unreachable s-t pairs','tratio-'+topo+'-1-'+Zinname+'-'+comp+'-ccdf.pdf',figurepath)
    #drawCDFandCCDF(dictx,dicty,6,0,'# unreachable s-t pairs','tratio-'+topo+'-1-'+Zinname+'-'+comp+'-ccdf.pdf',figurepath)
