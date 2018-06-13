using OhMyJulia
using DataFrames
using PyCall
using NaturalSort
using Fire
@pyimport gurobipy as grb

include("path.jl")
include("weight.jl")

const data_list = ["abilene", "Cernet", "Cesnet201006", "Chinanet", "Esnet", "Garr200112", "Grnet",
                   "Ibm", "jelly16", "Nordu1997", "Tinet"]
const algo_list = ["Ecmp", "Edksp", "Ksp", "Mcf", "Raeke", "Vlb"]

function read_topo(file)
    nodes, edges = Set{String}(), String[]
    for line in eachline(file) @when (m = match(r"(s\d+) -> (s\d+)", line)) != nothing
        push!(nodes, m[1], m[2])
        push!(edges, "$(m[1]) $(m[2])")
    end
    nodes, edges
end

function read_demand(hosts, demands)
    results = []
    hosts = readlines(hosts)
    n = length(hosts)
    for line in eachline(demands)
        line = map(x->parse(f64, x), split(line, ' '))
        demand = Dict{String, Float64}()
        for i in 1:n, j in 1:n @when i != j
            demand["$(hosts[i]) $(hosts[j])"] = line[(i-1) * n + j] / 2^20 # to Megabyte
        end
        push!(results, demand)
    end
    results
end

function read_budget(hosts, budgets)
    Dict(zip(map(x->replace(x, 'h', 's'), readlines(hosts)),
             map(x->parse(Int, x),        readlines(budgets))))
end

function write_scheme(io, scheme)
    for (pair, paths) in scheme
        println(io, pair, ':')
        for (path, w) in paths
            p = map(x->split(x, ' '), path)
            println(io, join(map(car, p) ++ cadr(p[end]), " -> "), " @ ", w)
        end
        println(io)
    end
end

@main function main(data)
    @assert data in data_list
    io, process = open(`yates -budget 16 $data`)
    path_sets = parse_schemes(io)
    nodes, edges = read_topo("data/$data.dot")
    demands = read_demand("data/$data.hosts", "data/$data.demands")
    budgets = read_budget("data/$data.hosts", "data/$data.budgets")
    
    for (i, demand) in enumerate(demands), algo in algo_list
        for (name, select) in (("program", select_program),
                               ("greedy", select_greedy),
                               ("hardnop", select_hard_nop))
            open("results/$data-$i-$algo-$name.result", "w") do fout
                raw_scheme = select(nodes, edges, path_sets[algo], budgets)
                m1_scheme, Z = minimize_maximum_link_utilization(nodes, edges, demand, raw_scheme)
                m2_scheme, Zs = minimize_maximum_link_utilization_then_maximize_throuput(nodes, edges, demand, raw_scheme)
                
                println(fout, "number of nodes (switch): ", length(nodes))
                println(fout, "number of edges (core): ", length(edges))
                println(fout, "number of demand pairs: ", length(demand))
                println(fout, "average budgets: ", mean(values(budgets)))
                println(fout)
                
                println(fout, "Z: ", Z)
                println(fout, "total throuput before the second step:", sum(values(demand)) / max(Z, 1))
                println(fout, "total throuput after the second step:", sum(d / Zs[pair] for (pair, d) in demand))
                println(fout)
                
                println(fout, "number of path through each node:")
                node_dict = Dict(n => 0 for n in nodes)
                for (pair, paths) in m2_scheme, (path, weight) in paths, edge in path
                    n = split(edge, ' ') |> car
                    if car(n) == 's'
                        node_dict[n] += 1
                    end
                end
                for (node, number) in sort(collect(node_dict), lt=natural, by=car)
                    println(fout, "  ", node, ": ", number)
                end
                println(fout, "  average: ", sum(values(node_dict)) / length(node_dict))
                println(fout)
                
                println(fout, "number of path, total flow, and link utiliaztion of each edge:")
                edge_dict = Dict(e => [] for e in edges)
                for (pair, paths) in m2_scheme, (path, weight) in paths, edge in path @when 'h' ∉ edge
                    push!(edge_dict[edge], demand[pair] * weight)
                end
                for (edge, flows) in sort(collect(edge_dict), lt=natural, by=car)
                    println(fout, "  ", edge, ": ", length(flows), ", ", sum(flows), ", ", sum(flows) / 10, '%')
                end
                println(fout, "  average: ", sum(length(v) for v in values(edge_dict)) / length(edge_dict), 
                                       ", ", sum(sum(v) for v in values(edge_dict)) / length(edge_dict),
                                       ", ", sum(sum(v) for v in values(edge_dict)) / length(edge_dict) / 10, '%')
                println(fout)
                
                println(fout, "number of path and demand ratio of each st pair:")
                pair_dict = Dict(pair => length(paths) for (pair, paths) in m2_scheme)
                for (pair, nflows) in sort(collect(pair_dict), lt=natural, by=car)
                    println(fout, "  ", pair, ": ", nflows, ", ", 1 / Zs[pair] * 100, '%')
                end
                println(fout, "  average: ", sum(values(pair_dict)) / length(pair_dict),
                                       ", ", sum(d / Zs[pair] for (pair, d) in demand) / sum(values(demand)) * 100, '%')
                println(fout)
                
                println(fout, "path set:")
                write_scheme(fout, path_sets[algo])
                println(fout)
                
                println(fout, "paths selected:")
                write_scheme(fout, raw_scheme)
                println(fout)
                
                println(fout, "paths after the first step (minimize maximum link utilization):")
                write_scheme(fout, m1_scheme)
                println(fout)
                
                println(fout, "paths after the second step (maximize total throuput):")
                write_scheme(fout, m2_scheme)
            end
        end
    end
end
