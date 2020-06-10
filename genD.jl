data_list = ["Cernet" , "Globalcenter" , "Goodnet" , "Gridnet" , "gscale" , "Janetbackbone" ,
"Rediris" , "Renater2010" , "Sinet" , "Sprint" , "SprintINET" , "Surfnet" ,
"SwitchL3" , "TataNld" , "Tinet" , "Uninett2011" , "Uunet" , "VtlWavenet2011" , "Xeex" , "Xspedius"]

function gen_gravity(data)
    hosts = readlines("data/$data.hosts")
    open("data/$data.demands", "w") do fout
        for k in 1:60
            #α = 2^(23 + k)
            α = 2^(24 + floor(k/10))
            weigths = map(x->rand(), hosts)
            list = [ α * weigths[i] * weigths[j]
                     for i in 1:length(hosts)
                     for j in 1:length(hosts) ]
            println(fout, join(list, ' '))
        end
    end
end
for i in data_list
    gen_gravity(i)
end
