#!/usr/bin/env julia

using OhMyJulia
using JSON

read_topo = true
node_list = String[]
node_dict = Dict{String, Int}()
topo = Set{Tuple{Int, Int}}()
demands = Tuple{Int, Int}[]

# requires switches and hosts numbers to be a 1 to 1 map
for line in readlines()
    if line == "***"
        read_topo = false
        continue
    end
    
    src, dst = split(line, ' ')
    src, dst = cdr(src), cdr(dst)
    src == dst && continue
        
    if read_topo
        for n in (src, dst)
            if n ∉ keys(node_dict)
                push!(node_list, n)
                node_dict[n] = length(node_list)
            end
        end
        push!(topo, (node_dict[src], node_dict[dst]))
    else
        push!(demands, (node_dict[src], node_dict[dst]))
    end
end

nnode = length(node_list)
        
if length(demands) == 0
    for i in 1:nnode, j in 1:nnode @when i != j
        push!(demands, (i, j))
    end
end

const lib = rel"a.out"

groups = []

tic()

for (src, dst) in demands
    mf = ccall((:init, lib), *(Void), (Cint,), nnode)

    for (s, d) in topo @when s < d
        ccall((:addEdge, lib), Void, (*(Void), Cint, Cint), mf, s, d)
    end
    
    max_flow = ccall((:dinitz, lib), Cint, (*(Void), Cint, Cint), mf, src, dst)
    npath = ccall((:npath, lib), Cint, (*(Void),), mf)
        
    group = []
    
    for i in 1:npath
        len = ccall((:path_len, lib), Cint, (*(Void), Cint), mf, i)
        path = Vector{Cint}(len)
        ccall((:get_path, lib), Void, (*(Void), Cint, *(Cint)), mf, i, path)
        push!(group, [src] ++ path)
    end
    
    push!(groups, group)
end

println(STDERR, "TIME: ", toq())

# println(STDERR, groups)

to_pair(x) = "h$(node_list[x[][]]) h$(node_list[x[][end]])"

to_path(x) = begin
    path = ["s$(node_list[x[i]]) s$(node_list[x[i+1]])" for i in 1:length(x)-1]
    hsrc = "h$(node_list[x[]]) s$(node_list[x[]])"
    hdst = "s$(node_list[x[end]]) h$(node_list[x[end]])"
    [hsrc, path..., hdst]
end

println(JSON.json(Dict( to_pair(group) => map(to_path, group) for group in groups )))
