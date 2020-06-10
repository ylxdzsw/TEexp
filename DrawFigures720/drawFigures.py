#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib

def drawFigure(Z, bandallostep1, bandallostep2, Zhardnop, hardbandallostep1, hardbandallostep2, figname, figurepath):#, topo, figname, figurepath):#, Zoptimal, Toptimal, Dnum):
    plt.rcParams['font.size'] = 10
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)

    #R3: Step 1. use minimize the maximum link utilization;
    #Step 2. when Step 1's result Z > 1, maximize the whole throughput with a new constrain TM/Z < TM' < TM

    bandallostep1 = [x/1000.0 for x in bandallostep1]#TODO normalize to optimal result
    bandallostep2 = [x/1000.0 for x in bandallostep2]

    s = sorted(zip(Z,bandallostep1,bandallostep2))
    Z,bandallostep1,bandallostep2 = map(list, zip(*s))


    #fig, ax = plt.subplots(figsize=(5.5,4.1))

    plt.xlabel('Z', fontsize=12)
    plt.ylabel('Whole Throughput (Gbps)', fontsize=12)#Cernet-1-Raeke-program.json ... Cernet-6-Raeke-program.json

    #TODO what is the unit of our EXP ? or doesn't matter? either Gbps or GB?

    line1, = plt.plot(Z, bandallostep2, color='orange', linestyle='--', marker='o', ms=8, linewidth=2.0, markerfacecolor='None')
    line2, = plt.plot(Z, bandallostep1, color='turquoise', linestyle='-', marker='*', ms=8, linewidth=2.0, markerfacecolor='None')


    hardbandallostep1 = [x/1000.0 for x in hardbandallostep1]
    hardbandallostep2 = [x/1000.0 for x in hardbandallostep2]

    s = sorted(zip(Zhardnop,hardbandallostep1,hardbandallostep2))
    Zhardnop,hardbandallostep1,hardbandallostep2 = map(list, zip(*s))


    # for i in range(Dnum):
    #     bandallostep1[i] = bandallostep1[i]*1.0/Toptimal[i] #TODO hard to get the optimal throughput after Z>1
    #     bandallostep2[i] = bandallostep2[i]*1.0/Toptimal[i]
    #     hardbandallostep1[i] = hardbandallostep1[i]*1.0/Toptimal[i]
    #     hardbandallostep2 = hardbandallostep2[i]*1.0/Toptimal[i]

    line3, = plt.plot(Zhardnop, hardbandallostep2, color='firebrick', linestyle='--', marker='v', ms=8, linewidth=2.0, markerfacecolor='None')
    line4, = plt.plot(Zhardnop, hardbandallostep1, color='steelblue', linestyle='-', marker='D', ms=8, linewidth=2.0, markerfacecolor='None')

    #TODO TODO here we need to show whole name of figure?
    #pp = PdfPages('/Users/run/Desktop/infocom2019code/fig/'+topo+'1/'+figname)#use parameter
    pp = PdfPages(figurepath+figname)#use parameter
    #pp = PdfPages('/Users/run/Desktop/infocom2019code/fig/'+topo+'/'+figname)#use parameter
    #figname=topo+"-"+alg+"-program-hardnop.pdf"
    algname=figname.split('-')[1]
    #ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6])
    #plt.legend((line1, line2, line3, line4),('TED ('+algname+',program)', 'Smore ('+algname+',program)', 'TED ('+algname+',hard)', 'Smore ('+algname+',hard, TM/Z if Z>1)'),loc='upper left')#, frameon=False)
    plt.legend((line2, line4, line1, line3),('Smore ('+algname+', program, TM/Z if Z>1)', 'Smore ('+algname+', hardnop, TM/Z if Z>1)', 'TED ('+algname+', program)', 'TED ('+algname+', hardnop)'),loc='upper left')

    plt.grid(True)

    plt.savefig(pp, format='pdf', dpi=600)
    #pp.savefig()
    pp.close()
    plt.show()
    plt.close()
    return


def drawBenefit(Zrelated,lessorlarge,lineN,xlabel,ylabel,figname,figurepath):
#lineN means draw N lines, also means dict xlist, ylist has N list, key is the alg name,
#Zless1={di: {'Optimal':0.9, 'Ksp':0.91, ...}, ...} Zlarge1={dj:{'Optimal':1.1, 'Ksp':[1.2, Tstep1, Tstep2], ...}, ...}

    linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','TM/Z (Ksp)':':'
    ,'TM (Ksp)':'--','TM/Z (Raeke)':':','TM (Raeke)':'--','TM/Z (Edksp)':':','TM (Edksp)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    #linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--'}#TODO this can be modified

    markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
    'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}#TODO consider whether we need optimal?

    #colors = {'Custom':'r','Raeke':'b','Edksp':'g','Ksp':'m','Ecmp':'c','Vlb':'y'}#,'Mcf':'w','Optimal':'k','TM/Z':'w','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
    colors = {'Custom':'firebrick','Raeke':'steelblue','Edksp':'g','Ksp':'darkorange','Ecmp':'c','Vlb':'y'}

    #'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}#TODO consider whether we need optimal?

    #markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+'}

    algdic=[]
    if lineN==4:
        algdic=["Raeke","Edksp","Ksp","Custom"]#["Ksp","Custom","Edksp","Raeke"]#TODO add our custom
    else:
        #algdic=["Ksp","Custom","Ecmp","Edksp","Raeke","Vlb"]#,"Mcf"]#TODO add our custom
        #algdic=["Custom","Edksp","Raeke","Vlb","Ksp","Ecmp"]
        algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]
    plt.rcParams['font.size'] = 10
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)

    #fig, ax = plt.subplots(figsize=(5.5,4.1))
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    lines=[]
    labels=[]
    if lessorlarge:
        for key in algdic:#xlist:
            x = [Zrelated[d]['Optimal'] for d in Zrelated]
            y = [Zrelated[d][key]/Zrelated[d]['Optimal'] for d in Zrelated]

            s = sorted(zip(x,y))
            x,y = map(list, zip(*s))


            #linetemp, = plt.plot(x, y, linestyle='--', marker='v', ms=8, linewidth=2.0)
            linetemp, = plt.plot(x, y, color=colors[key], linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0, markerfacecolor='None')#, markevery=10)
            #linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=6, linewidth=1.5)#, markevery=10)
            lines.append(linetemp)
            labels.append(key)
    else:
        for key in algdic:#xlist:
            x = [Zrelated[d]['Optimal'] for d in Zrelated]
            y = [Zrelated[d][key][2]*Zrelated[d]['Optimal']/Zrelated[d][key][0]/Zrelated[d][key][1] for d in Zrelated]#T/(sum(TM)/Zopt)
            #y = [Zrelated[d][key][2]/Zrelated[d][key][0]/Zrelated[d][key][1] for d in Zrelated]#TODO this should be? TM or TM/Zopt? (TODO)
            #y = [Zrelated[d][key][0] for d in Zrelated]
            print x,y
            s = sorted(zip(x,y))
            x,y = map(list, zip(*s))
            print x,y
            #del x[-1]
            #del y[-1]
            #linetemp, = plt.plot(x, y, linestyle='--', marker='v', ms=8, linewidth=2.0)
            linetemp, = plt.plot(x, y, color=colors[key], linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0, markerfacecolor='None')#, markevery=10)
            #linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=6, linewidth=1.5)#, markevery=10)
            lines.append(linetemp)
            labels.append(key)
    #handles, labels = plt.get_legend_handles_labels()#TODO test this

    #pp = PdfPages('/home/zhangshiwei/jupyter/yates4/analysispy/PerformanceRatio/'+figname)#use parameter
    #pp = PdfPages('/Users/run/Desktop/infocom2019code/PerformanceRatio/'+figname)
    pp = PdfPages(figurepath+figname)

    #TODO TODO use parameter ? like figure save path?

    print lines,labels
    #plt.legend(handles, labels)#TODO test this
    plt.legend(lines, labels, loc='upper left')#,frameon=False)#'lower right')#, ncol=5)#, loc='upper left')
    plt.grid(True)

    plt.savefig(pp, format='pdf', dpi=600)
    #pp.savefig()
    pp.close()
    plt.show()
    plt.close()#TODO TODO test this one
