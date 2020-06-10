import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
#TODO not ready yet
#algdic=["Ksp","Custom","Ecmp","Edksp","Raeke","Vlb","Mcf"]#TODO add our custom
#algdic=["Ksp","Custom","Edksp","Raeke"]#TODO add our custom

#name_list = ["P(D > 90%)","P(D > 95%)","P(D > 99%)","P(D > 99.9%)","P(D > 99.99%)"]#["Ksp","Custom","Edksp","Raeke"]#['Monday','Tuesday','Friday','Sunday']
#name_list = ["P(D'>90%)","P(D'>95%)","P(D'>99%)","P(D'>99.9%)","P(D'>99.99%)"]#["Ksp","Custom","Edksp","Raeke"]#['Monday','Tuesday','Friday','Sunday']
name_list = ["P(D>90%)","P(D>95%)","P(D>99%)","P(D>99.9%)","P(D>99.99%)"]

#algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]
#algdic=["Raeke","Ksp","Vlb","Edksp","Custom"]
algdic=["Vlb","Edksp","Custom","Raeke","Ksp","Ecmp"]

#algdic=["Vlb","Edksp","Custom","Raeke","Ksp"]

linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','TM/Z (Ksp)':':'
    ,'TM (Ksp)':'--','TM/Z (Raeke)':':','TM (Raeke)':'--','TM/Z (Edksp)':':','TM (Edksp)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    #linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--'}#TODO this can be modified

markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
    'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}#TODO consider whether we need optimal?

    #colors = {'Custom':'r','Raeke':'b','Edksp':'g','Ksp':'m','Ecmp':'c','Vlb':'y'}#,'Mcf':'w','Optimal':'k','TM/Z':'w','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
colors = {'Custom':'firebrick','Raeke':'steelblue','Edksp':'g','Ksp':'darkorange','Ecmp':'c','Vlb':'y'}
#Zopt<=1
#algstdratioH={'Raeke': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Ksp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Vlb': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Custom': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Edksp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.9772727272727273, 0.9696969696969697], 'Ecmp': [0.9924242424242424, 0.9924242424242424, 0.9848484848484849, 0.8484848484848485, 0.8409090909090909]}
algstdratioH={'Raeke': [0.5075757575757576, 0.4621212121212121, 0.3712121212121212, 0.3560606060606061, 0.3484848484848485], 'Ksp': [0.5, 0.4772727272727273, 0.3712121212121212, 0.36363636363636365, 0.3560606060606061], 'Vlb': [0.5075757575757576, 0.4772727272727273, 0.3939393939393939, 0.38636363636363635, 0.3787878787878788], 'Custom': [0.5075757575757576, 0.4696969696969697, 0.3939393939393939, 0.3712121212121212, 0.36363636363636365], 'Edksp': [0.5151515151515151, 0.45454545454545453, 0.36363636363636365, 0.3333333333333333, 0.32575757575757575], 'Ecmp': [0.4393939393939394, 0.30303030303030304, 0.26515151515151514, 0.25757575757575757, 0.25]}
#Zopt>1

x =list(range(len(name_list)))
total_width, n = 0.7, 6
width = total_width / n

#plt.ylim(ymin=0.75,ymax=1.035)
plt.ylim(ymin=0.2,ymax=0.54)
for i in range(len(algdic)):
    key=algdic[i]
    xtemp=range(len(name_list))
    for j in range(len(x)):
        xtemp[j] = x[j] + width*i
    y=algstdratioH[key]
    color=colors[key]
    print x,y
    #linetemp, =
    if i==3:
        plt.bar(xtemp, y, width=width, label=key, tick_label = name_list, fc=color)#, linestyle=linestyles[key], marker=markers[key], ms=8, linewidth=2.0)#, markevery=10)
    else:
        plt.bar(xtemp, y, width=width, label=key, fc=color)
            #linetemp, = plt.plot(x, y, linestyle=linestyles[key], marker=markers[key], ms=6, linewidth=1.5)#, markevery=10)
    #lines.append(linetemp)
    #labels.append(key)
#plt.bar(x, num_list, width=width, label=algdic[key],fc = 'b')
#for i in range(len(x)):
#    x[i] = x[i] + width
#plt.bar(x, num_list1, width=width, label='Step 2: Maximize(whole throughput) with TM/Z<TM\'<TM',tick_label = name_list,fc = 'r')
#pp = PdfPages('/Users/run/Desktop/infocom2019code/DrawFigures714/fig/test/fairnesszless1.pdf')
pp = PdfPages('/Users/run/Desktop/infocom2019code/DrawFigures714/fig/test/fairnesszlarge1.pdf')

plt.legend(ncol=3)
plt.savefig(pp, format='pdf', dpi=600)
#pp.savefig()
pp.close()
plt.show()
