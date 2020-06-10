#the CDF and CCDF functions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib

def ccdf(data):
    body = ''
    y=[]
    data.sort()
    x=data
    for i, v in enumerate(data):
        #body += "({}, {})\n".format(v, (len(data) - i)*1.0/len(data))#P(X>=v)=y
        body += "({}, {})\n".format(v, (len(data) - i - 1)*1.0/len(data))#P(X>v)=y
        #y.append((len(data) - i)*1.0/len(data))
        y.append((len(data) - i - 1)*1.0/len(data))
    print x,y
    return x,y
    #with open('ccdf.tex', 'w') as fout:
    #    fout.write(head + body + foot)

def cdf(data):
    body = ''
    y=[]
    data.sort()
    x=data
    for i, v in enumerate(data):
        #body += "({}, {})\n".format(v, i*1.0/len(data))#P(X<v)=y
        #y.append(i*1.0/len(data))
        body += "({}, {})\n".format(v, (i+1)*1.0/len(data))#P(X<=v)=y
        y.append((i+1)*1.0/len(data))
    print x,y
    return x,y
    #with open('cdf.tex', 'w') as fout:
    #    fout.write(head + body + foot)

def drawCDFandCCDF(xlist,ylist,lineN,CDForCCDF,xlabel,figname,figurepath):
#lineN means draw N lines, also means dict xlist, ylist has N list, key is the alg name,
#xlist[algi], ylist[algi] for line i, with corresponding legend and linestyle and marker
#xlabel stands for the label of x axis, like flow entry or link congestion
    #linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','TM/Z (Ksp)':':',
    'TM (Ksp)':'--','TM/Z (Raeke)':':','TM (Raeke)':'--','TM/Z (Edksp)':':','TM (Edksp)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3'
    ,'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}

    #colors = {'Custom':'r','Raeke':'b','Edksp':'g','Ksp':'m','Ecmp':'c','Vlb':'y'}
    colors = {'Custom':'firebrick','Raeke':'steelblue','Edksp':'g','Ksp':'darkorange','Ecmp':'c','Vlb':'y'}

    algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]
    #markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','Minimize(max(le))':'p'}#TODO consider whether we need optimal?
    if CDForCCDF:
        #draw CDF, notice the label of y axis
        ylabel='CDF'
    else:
        #draw CCDF
        ylabel='CCDF'
    plt.rcParams['font.size'] = 10
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)

    #fig, ax = plt.subplots(figsize=(5.5,4.1))
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)#Cernet-1-Raeke-program.json ... Cernet-6-Raeke-program.json
    lines=[]
    labels=[]
    if lineN==6:
        for key in algdic:
            x = xlist[key]
            y = ylist[key]

            #linetemp, = plt.plot(x, y, linestyle='--', marker='v', ms=8, linewidth=2.0)
            linetemp, = plt.plot(x, y, color=colors[key], linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0, markerfacecolor='None')#, markevery=10)
            #linetemp, = plt.plot(x, y, color=colors[key], linestyle=linestyles[key], marker=markers[key], ms=5, linewidth=1.5)#, markevery=10)
            lines.append(linetemp)
            labels.append(key)
    else:
        for key in xlist:
            x = xlist[key]
            y = ylist[key]

            #linetemp, = plt.plot(x, y, linestyle='--', marker='v', ms=8, linewidth=2.0)
            linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0, markerfacecolor='None')#, markevery=10)
            #linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=4, linewidth=1.5)#, markevery=10)
            lines.append(linetemp)
            labels.append(key)

    #handles, labels = plt.get_legend_handles_labels()#TODO test this

    #pp = PdfPages('/Users/run/Desktop/infocom2019code/CDF/'+figname)#use parameter
    pp = PdfPages(figurepath+figname)#use parameter

    #ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6])

    #plt.legend(handles, labels)#TODO test this
    if CDForCCDF:
        plt.legend(lines, labels, loc='upper left')#, frameon=False)
    else:
        plt.legend(lines, labels, loc='upper right')#, frameon=False)
    plt.grid(True)

    plt.savefig(pp, format='pdf', dpi=600)
    #pp.savefig()
    pp.close()
    plt.show()
    plt.close()
