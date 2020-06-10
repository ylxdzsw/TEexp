import matplotlib.pyplot as plt
#TODO not ready yet
#algdic=["Ksp","Custom","Ecmp","Edksp","Raeke","Vlb","Mcf"]#TODO add our custom
#algdic=["Ksp","Custom","Edksp","Raeke"]#TODO add our custom

name_list = ["P(T > 90%)","P(T > 95%)","P(T > 99%)","P(T > 99.9%)","P(T > 99.99%)"]#["Ksp","Custom","Edksp","Raeke"]#['Monday','Tuesday','Friday','Sunday']

algdic=["Raeke","Ksp","Vlb","Ecmp","Edksp","Custom"]

linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--','TM/Z (Ksp)':':'
    ,'TM (Ksp)':'--','TM/Z (Raeke)':':','TM (Raeke)':'--','TM/Z (Edksp)':':','TM (Edksp)':'--','Minimize(max(le))':'-.'}#TODO this can be modified
    #linestyles = {'Custom':'-','Raeke':'-','Edksp':'-','Ksp':'-','Ecmp':'-','Vlb':'-','Mcf':'-','Optimal':'-','TM/Z':':','TM/Z (Custom)':':','TM (Custom)':'--'}#TODO this can be modified

markers = {'Custom':'v','Raeke':'D','Edksp':'o','Ksp':'*','Ecmp':'^','Vlb':'P','Mcf':'x','Optimal':'s','TM/Z':'.','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
    'TM (Ksp)':'4','TM/Z (Raeke)':'2','TM (Raeke)':'1','TM/Z (Edksp)':'<','TM (Edksp)':'>','Minimize(max(le))':'p'}#'TM/Z (Ksp)':'tri_left','TM (Ksp)':'tri_right','TM/Z (Raeke)':'tri_up','TM (Raeke)':'tri_down','TM/Z (Edksp)':'triangle_left','TM (Edksp)':'triangle_right','Minimize(max(le))':'p'}#TODO consider whether we need optimal?

    #colors = {'Custom':'r','Raeke':'b','Edksp':'g','Ksp':'m','Ecmp':'c','Vlb':'y'}#,'Mcf':'w','Optimal':'k','TM/Z':'w','TM/Z (Custom)':'.','TM (Custom)':'+','TM/Z (Ksp)':'3',
colors = {'Custom':'firebrick','Raeke':'steelblue','Edksp':'g','Ksp':'darkorange','Ecmp':'c','Vlb':'y'}


algetratioH={'Raeke': [0.8397660818713447, 0.8374269005847951, 0.8339181286549705, 0.8327485380116956, 0.8327485380116956], 'Ksp': [0.7894736842105268, 0.7894736842105268, 0.7859649122807022, 0.7847953216374273, 0.7847953216374273], 'Vlb': [0.9789473684210523, 0.9672514619883039, 0.9578947368421051, 0.9555555555555554, 0.9555555555555554], 'Custom': [0.9789473684210523, 0.9684210526315786, 0.9532163742690056, 0.9461988304093563, 0.9461988304093563], 'Edksp': [0.9789473684210523, 0.9695906432748536, 0.9578947368421051, 0.949707602339181, 0.9485380116959061], 'Ecmp': [0.0, 0.0, 0.0, 0.0, 0.0]}

x =list(range(len(name_list)))
total_width, n = 0.7, 6
width = total_width / n

for i in range(len(algdic)):
    key=algdic[i]
    xtemp=range(len(name_list))
    for j in range(len(x)):
        xtemp[j] = x[j] + width*i
    y=algetratioH[key]
    color=colors[key]
    print x,y
    #linetemp, =
    if i==0:
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
plt.legend()
plt.show()
