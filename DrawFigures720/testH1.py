import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
#TODO not ready yet
#algdic=["Ksp","Custom","Ecmp","Edksp","Raeke","Vlb","Mcf"]#TODO add our custom
#algdic=["Ksp","Custom","Edksp","Raeke"]#TODO add our custom
#TODO for robustness
name_list = ["P(T>90%)","P(T>95%)","P(T>99%)","P(T>99.9%)","P(T>99.99%)"]#["Ksp","Custom","Edksp","Raeke"]#['Monday','Tuesday','Friday','Sunday']

#algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]
#algdic=["Raeke","Ksp","Vlb","Edksp","Custom"]
algdic=["Vlb","Edksp","Custom","Raeke","Ksp"]

linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','TM/Z (Ksp)':':'
    ,'TM (Ksp)':'--','TM/Z (Raeke)':':','TM (Raeke)':'--','TM/Z (Edksp)':':','TM (Edksp)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    #linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--'}#TODO this can be modified

markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
    'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}#TODO consider whether we need optimal?

    #colors = {'Custom':'r','Raeke':'b','Edksp':'g','Ksp':'m','Ecmp':'c','Vlb':'y'}#,'Mcf':'w','Optimal':'k','TM/Z':'w','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
colors = {'Custom':'firebrick','Raeke':'steelblue','Edksp':'g','Ksp':'darkorange','Ecmp':'c','Vlb':'y'}

#algstdratioH={'Raeke': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Ksp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Vlb': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Custom': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Edksp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Ecmp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.8484848484848485, 0.8409090909090909]}
#Z<=1
#algetratioH={'Raeke': [0.8397660818713447, 0.8374269005847951, 0.8339181286549705, 0.8327485380116956, 0.8327485380116956], 'Ksp': [0.7894736842105268, 0.7894736842105268, 0.7859649122807022, 0.7847953216374273, 0.7847953216374273], 'Vlb': [0.9789473684210523, 0.9672514619883039, 0.9578947368421051, 0.9555555555555554, 0.9555555555555554], 'Custom': [0.9789473684210523, 0.9684210526315786, 0.9532163742690056, 0.9461988304093563, 0.9461988304093563], 'Edksp': [0.9789473684210523, 0.9695906432748536, 0.9578947368421051, 0.949707602339181, 0.9485380116959061], 'Ecmp': [0.0, 0.0, 0.0, 0.0, 0.0]}

algetratioH={'Raeke': [0.7587719298245613, 0.6710526315789473, 0.5570175438596491, 0.5043859649122806, 0.5043859649122806], 'Ksp': [0.7105263157894738, 0.6535087719298246, 0.5307017543859649, 0.4780701754385965, 0.4780701754385965], 'Vlb': [0.7938596491228069, 0.6666666666666666, 0.513157894736842, 0.4561403508771929, 0.4473684210526316], 'Custom': [0.7982456140350876, 0.6710526315789473, 0.5350877192982456, 0.4868421052631579, 0.4868421052631579], 'Edksp': [0.7982456140350876, 0.6929824561403509, 0.5570175438596492, 0.5043859649122806, 0.5043859649122806], 'Ecmp': [0.0, 0.0, 0.0, 0.0, 0.0]}
#Z>1
x =list(range(len(name_list)))
total_width, n = 0.8, 6
width = total_width / n

#plt.ylim(ymin=0.75)
plt.ylim(ymin=0.2, ymax=0.82)
for i in range(len(algdic)):
    key=algdic[i]
    xtemp=range(len(name_list))
    for j in range(len(x)):
        xtemp[j] = x[j] + width*i
    y=algetratioH[key]
    color=colors[key]
    print x,y
    #linetemp, =
    if i==2:
        plt.bar(xtemp, y, width=width, label=key, tick_label = name_list, fc=color)#, linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0)#, markevery=10)
        #plt.bar(xtemp, y, width=width, label=key, tick_label = name_list, edgecolors=color, c='w')
    else:
        plt.bar(xtemp, y, width=width, label=key, fc=color)
        #plt.bar(xtemp, y, width=width, label=key, edgecolors=color, c='w')
            #linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=6, linewidth=1.5)#, markevery=10)
    #lines.append(linetemp)
    #labels.append(key)
#plt.bar(x, num_list, width=width, label=algdic[key],fc = 'b')
#for i in range(len(x)):
#    x[i] = x[i] + width
#plt.bar(x, num_list1, width=width, label='Step 2: Maximize(whole throughput) with TM/Z<TM\'<TM',tick_label = name_list,fc = 'r')
#pp = PdfPages('/Users/run/Desktop/infocom2019code/DrawFigures714/fig/test/TradiosinglelfailZless1.pdf')
#pp = PdfPages('/Users/run/Desktop/infocom2019code/DrawFigures714/fig/test/TradiosinglelfailZlarge1.pdf')
pp = PdfPages('/home/run/Desktop/teda3/yates6/DrawFigures720/figCernet/TradiosinglelfailZlarge1.pdf')

plt.legend(ncol=3)
plt.savefig(pp, format='pdf', dpi=600)
#pp.savefig()
pp.close()
plt.show()
