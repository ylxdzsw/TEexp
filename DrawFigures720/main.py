#input the file path
#decide our maximum number of edge disjoint path should call what in the legend? Custom or ?
#TODO decide to show which algs
#TODO adjust the legend
#summarize we want which kind of figures
#1. Z<=1 the performance ratio     # analysisZ(demands, pathpre, topo, algdic, compare, figurepath)
#2. Z>1 the throughput ratio       # analysisZ(demands, pathpre, topo, algdic, compare, figurepath)
#3. the performance increase for each alg?  # analysisAlgT(demands, pathpre, topo, alg, figurepath)
#compare the whole throughput between step 1: min(max(le)) with step 2: maximize whole network throughput ?
#4. path utilization CDF           # analysisPaths(Zless1,demands, pathpre, topo, algdic, compare, figurepath)
#5. flow entries CCDF              # analysisFlowEntries(d, pathpre, topo, algdic, comp, figurepath)
#6. link utilizations CDF for alg comparison, and for step 1, step 2, optimal comparison (like for Custom)
# analysisLinksU(d, demandd, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']
# analysisAlgsLinksU(d, pathpre, topo, algdic, comp, figurepath)
#7. fairness: each s-t satisfied how many demands
#8. robustness: after single link failure, data plane reacting (TODO can satisfy how many rerouting traffic and loss how many)
#after single link failure, control plane reacting: throughput after recomputing TE
#9. computing time
#10. latency (path length or better use gscale testbed to get the real data TODO)
#11. reacting to TM changes? or path updating or?

#python main.py -p /Volumes/Transcend/infocom/yates5related/results/ -t gscale -dp /Users/run/Desktop/infocom2019code/yate40629/TEexp-master/data/ -fp /Users/run/Desktop/infocom2019code/DrawFigures714/fig/

#TODO TODO 2018.07.16
#1. get path utilization when Z<=1 for program done
#2. get the average path length done
#3. get throughput after single link failure TODO
#4. get the computing time (or just redraw the figure) done
#5. get the average ... for different topologies TODO

#TODO TODO 2018.07.17
#1. fairness: get the satisfied demand ratio (%) for each s-t pair, consider whether include Zopt<=1(will mostly be 1) , Z>1
#2. robustness: as we have shown that each s-t almost all use 1 path only (only one path has weight)
#therefore, we are hard to reroute in data plane use the normalized weight (TODO or just send packet out using equal weight to each healthy tunnel), ? TODO,
#2.1 get the percent that how many single link failure lead to some s-t pair unreachable
#2.2 get the Histogram of P(T>95%), P(T>95%), P(T>95%), P(T>95%), P(T>95%)
#2.3 get the throughput ratio CDF
from readJSON import readJSON
from readOptimal import readOptimal
#from drawFigures import drawFigure, drawBenefit
from analysisExps import *#TODO?

import argparse
parser = argparse.ArgumentParser()
#parser.add_argument("-a", "--alg", help="specify the path selection algorithm to use: Ksp, Custom, Ecmp, Edksp, Raeke, Vlb, Mcf")
#parser.add_argument("-c", "--comp", help="specify the used comparison method: greedy, hardnop, program")
#parser.add_argument("-t", "--topo", help="specify the used topology: abilene, gscale, Cernet, Cesnet201006, Chinanet, Esnet, Garr200112, Grnet, Ibm, jelly16, Nordu1997, Sprint, Tinet")

#parser.add_argument("-a", "--alg", help="Ksp, Custom, Ecmp, Edksp, Raeke, Vlb, Mcf")
#parser.add_argument("-c", "--comp", help="greedy, hardnop, program")
parser.add_argument("-p", "--path", help="the path of json files, e.g., /Volumes/Transcend/infocom/yates5related/results/ for gscale")
parser.add_argument("-t", "--topo", help="abilene, gscale, Cernet, Cesnet201006, Chinanet, Esnet, Garr200112, Grnet, Ibm, jelly16, Nordu1997, Sprint, Tinet")
parser.add_argument("-dp", "--demandpath", help="the path of alg.demands files")
parser.add_argument("-fp", "--figurepath", help="the path to save figures")
#parser.add_argument("-o", "--opti", help="optimal mcf") #TODO include the optimal or not?

args = parser.parse_args()
#if args.alg:
#    print args.alg
#if args.comp:#TODO consider whether to use this one
#    print args.comp
if args.path:
    print args.path
if args.topo:
    print args.topo
if args.demandpath:
    print args.demandpath
if args.figurepath:
    print args.figurepath

#algdic=["Ksp","Custom","Ecmp","Edksp","Raeke","Vlb"]#,"Mcf"]
#algdic=["Custom","Edksp","Raeke","Vlb","Ksp","Ecmp"]
algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]
#TODO consider the name of our custom and readjust the position, legend of each alg
#algdic=["Raeke","Edksp","Ksp","Custom"]
#algdic=["Ksp","Custom","Edksp","Raeke"]
demands=range(1,61)#[1,2,3,4,5,6]
#compare=["greedy","hardnop","program"]#TODO for largescale like number of switch>16 ... greedy not work
pathpre=args.path#"/Volumes/Transcend/infocom/yates5related/results/"
#pathpre="/Users/run/Desktop/infocom2019code/yate40629/TEexp-master/results/"
#pathpre="/home/zhangshiwei/jupyter/yates4/results/Cernet0704/"
topo=args.topo#"gscale"#["abilene","gscale","Cernet","Cesnet201006","Chinanet",
#"Esnet","Garr200112","Grnet","Ibm","jelly16","Nordu1997","Sprint","Tinet"]
dpath=args.demandpath#/Users/run/Desktop/infocom2019code/yate40629/TEexp-master/data/
#TODO here we only need to call the analysis functions in analysisExps.py,
#so that we can get all the figures directly from the results' JSON files
figurepath=args.figurepath
#TODO TODO 1. select a dth demand which Custom's Z ~= 1.5, 2. compute the dth demand
#3. get the figure which draws the link utilization of TM, TM/Z, TM optimal, Custom TM'
hostsfile=open(dpath+topo+'.hosts')
lines=hostsfile.readlines()
hosts=[v.split('\n')[0] for v in lines]
print hosts
compare=[]
if len(hosts)<16:
    compare=["greedy","hardnop","program"]#TODO for largescale like number of switch>16 ... greedy not work
else:
    compare=["hardnop","program"]

comp="hardnop"
Zless1, Zlarge1 = analysisZ(demands, pathpre, topo, algdic, comp, figurepath)#compare, figurepath)
comp="program"
analysisZ(demands, pathpre, topo, algdic, comp, figurepath)#TODO
for alg in algdic:
    analysisAlgT(demands, pathpre, topo, alg, figurepath)
comparetemp=["hardnop"]
analysisPaths(Zless1, demands, pathpre, topo, algdic, comparetemp, figurepath)

analysisPathlength(Zless1, demands, pathpre, topo, algdic, comparetemp, figurepath)

lessorlargeorall=1
analysisPathlength1(Zless1, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)
lessorlargeorall=2
analysisPathlength1(Zlarge1, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)
lessorlargeorall=3
analysisPathlength1(demands, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)


comparetemp=["program"]
analysisPaths(Zless1, demands, pathpre, topo, algdic, comparetemp, figurepath)
analysisPathlength(Zless1, demands, pathpre, topo, algdic, comparetemp, figurepath)

lessorlargeorall=1
analysisPathlength1(Zless1, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)
lessorlargeorall=2
analysisPathlength1(Zlarge1, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)
lessorlargeorall=3
analysisPathlength1(demands, lessorlargeorall, demands, pathpre, topo, algdic, comparetemp, figurepath)


d=1
for comp in compare:
    analysisFlowEntries(d, pathpre, topo, algdic, comp, figurepath)
#Zlarge1[d]['Optimal']=Z
dth=0
for d in Zlarge1:
    if d==0:
        dth=d
    else:
        filename=pathpre+topo+"-"+str(d)+"-Custom-hardnop.json"#"-"+str(d)+"-optimal-mcf.json"
        #fileOptimal=readOptimal(filename)
        #Z=fileOptimal['Z']
        fileJSON=readJSON(filename)
        Z=fileJSON['Z']
        if Z<1.6 and Z>1.4:
            dth=d
            break

if dth==0:
    if len(Zlarge1)<>0:
        dth=min(Zlarge1)
    else:
        print 'no file with Z>1'
        dth=max(Zless1)

filename=pathpre+topo+"-"+str(dth)+"-Custom-hardnop.json"
fileJSON=readJSON(filename)
Z=fileJSON['Z']
print 'file '+str(dth)+' is analyzed and Z is '+str(Z)
        #return
#TODO if there is no file with 1.4<Z<1.6, then select one with 1<Z<2? if there is no file with Z>1, then return?

    #select a dth demand whose Z~=1.5
#get dth demand
#TODO test dth
#if topo=="gscale":
#    dth=49
#elif topo=="Cernet":
#    dth=57#57 for Cernet and 49 for gscale
dthfile=open(dpath+topo+'.demands')
lines=dthfile.readlines()
demanddtemp=lines[dth-1].split()
demandd=[float(v) for v in demanddtemp]
print 'demand ',demandd
hostsdemand={}
n=len(hosts)
for i in range(n):
    for j in range(n):
        if i<>j:
            hostsdemand[hosts[i]+' '+hosts[j]]=demandd[i*n+j]
#comp="hardnop"
for comp in compare:
    analysisAlgsLinksU(dth, pathpre, topo, algdic, comp, figurepath)
comp="hardnop"
algdic=["Custom"]
#analysisLinksU(dth, demand49gscale, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']
#analysisLinksU(dth, demandd, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']
analysisLinksU(dth, hostsdemand, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']

algdic=["Raeke"]
#analysisLinksU(dth, demandd, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']
analysisLinksU(dth, hostsdemand, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']

#analysisLinksU(dth, demand49gscale, pathpre, topo, algdic, comp, figurepath) # algdic=['Custom']
print 'file '+str(dth)+' is analyzed and Z is '+str(Z)
