using OhMyJulia
using DataFrames
using PyCall
using NaturalSort
using Fire
using JSON
@pyimport gurobipy as grb

include("path.jl")
include("weight.jl")

const data_list = ["abilene", "gscale", "Cernet", "Cesnet201006", "Chinanet", "Esnet", "Garr200112",
                   "Grnet", "Ibm", "jelly16", "Nordu1997", "Sprint", "Tinet"]
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

function write_scheme(io, scheme, x=Dict())
    for (pair, paths) in scheme
        println(io, pair, ':')
        x[pair] = xx = Dict()
        for (path, w) in paths
            p = map(x->split(x, ' '), path)
            println(io, join(map(car, p) ++ cadr(p[end]), " -> "), " @ ", w)
            xx[join(map(car, p) ++ cadr(p[end]), " -> ")] = w
        end
        println(io)
    end
end

function optimal_mcf(nodes, edges, demand)
    tpair(pair) = split(replace(pair, 'h', 's'), ' ')
    
    le = Dict(e => Dict() for e in edges)

    conn = Dict(n => (
        [s for s in nodes if "$s $n" in edges],
        [t for t in nodes if "$n $t" in edges]
    ) for n in nodes)
    
    m = grb.Model("optimal_mcf")
    m[:setParam]("OutputFlag", false)
    Z = m[:addVar](name="Z")
    
    for (pair, d) in demand
        u, v = tpair(pair)
        luv = Dict(e => (le[e][pair] = m[:addVar](name="l_$(e)_$(u)_$(v)")) for e in edges)
        m[:update]()
        
        # constraint 1: influx == outflux for core nodes 
        for n in nodes @when n ∉ (u, v)
            ti = [luv["$u $n"] for u in car(conn[n])]
            to = [luv["$n $v"] for v in cadr(conn[n])]

            m[:addConstr](py"sum($ti) == sum($to)")
        end

        # constraint 2: demands are fulfilled
        x = [luv["$u $v"] for u in car(conn[v])]
        m[:addConstr](py"sum($x) == $d")
                                            
        x = [luv["$u $v"] for v in cadr(conn[u])]
        m[:addConstr](py"sum($x) == $d")
    end

    # constraint 3: minimize maximum link utilization
    for (edge, flows) in le
        flows = collect(values(flows))
        m[:addConstr](py"sum($flows) <= 1000 * $Z")
    end

    m[:setObjective](Z)
    m[:optimize]()

    json = Dict("Z" => m[:getObjective]()[:getValue]())
                                        
    for (edge, flows) in le, (pair, flow) in flows
        json["$pair $edge"] = flow[:X]
    end

    json
end
                                    
function single_failure(nodes, edges, demand, scheme)
    rev(x) = join(reverse(split(x, ' ')), ' ')

    stat(edges, scheme) = begin
        m1_scheme, Z = minimize_maximum_link_utilization(nodes, edges, demand, scheme)
        m2_scheme, Zs = minimize_maximum_link_utilization_then_maximize_throuput(nodes, edges, demand, scheme)
        Z, sum(d / Zs[pair] for (pair, d) in demand)
    end

    json = Dict()

    for e in edges @when (<)(split(e, ' ')...)
        edges_f = filter(x->x ∉ (e, rev(e)), edges)
        scheme_f = Dict()
        for (pair, paths) in scheme
            paths_f = [(path, weight) for (path, weight) in paths if e ∉ path && rev(e) ∉ path]
            # no need to renormalize since we will overwrite them anyway
            isempty(paths_f) && @goto disconnected
            scheme_f[pair] = paths_f
        end

        json[e] = stat(edges_f, scheme_f)
        continue

        @label disconnected
        json[e] = "some pairs have no path"
    end

    json
end

@main function main(data; optimal::Bool=false)
    @assert data in data_list
    io, process = open(`yates -budget 16 $data`)
    path_sets = parse_schemes(io)
    nodes, edges = read_topo("data/$data.dot")
    demands = read_demand("data/$data.hosts", "data/$data.demands")
    budgets = read_budget("data/$data.hosts", "data/$data.budgets")
    
    for (i, demand) in enumerate(demands)
        if optimal
            open("results/$data-$i-optimal-mcf.json", "w") do fout
                JSON.print(fout, optimal_mcf(nodes, edges, demand), 2)
            end
            continue
        end
            
        for algo in algo_list, (name, select) in (("program", select_program),
                                                  ("greedy", select_greedy),
                                                  ("hardnop", select_hard_nop)) @when length(nodes) < 16 || name != "greedy"
            json = Dict()
            
            open("results/$data-$i-$algo-$name.result", "w") do fout
                tic()
                raw_scheme = select(nodes, edges, path_sets[algo], budgets)
                time1 = toq()
                
                any(isempty, values(raw_scheme)) && return println(fout, "cannot solve")
                
                tic()
                m1_scheme, Z = minimize_maximum_link_utilization(nodes, edges, demand, raw_scheme)
                time2 = toq()
                
                tic()
                m2_scheme, Zs = minimize_maximum_link_utilization_then_maximize_throuput(nodes, edges, demand, raw_scheme)
                time3 = toq()
                
                
                println(fout, "number of nodes (switch): ", length(nodes))
                json["number of nodes (switch)"] = length(nodes)
                
                println(fout, "number of edges (core): ", length(edges))
                json["number of edges (core)"] = length(edges)
                
                println(fout, "number of demand pairs: ", length(demand))
                json["number of demand pairs"] = length(demand)
                
                println(fout, "average budgets: ", mean(values(budgets)))
                json["average budgets"] = mean(values(budgets))
                
                println(fout)
                
                
                println(fout, "time elapsed during path selection: ", time1, 's')
                json["time elapsed during path selection"] = time1
                
                println(fout, "time elapsed during first step: ", time2, 's')
                json["time elapsed during first step"] = time2
                
                println(fout, "time elapsed during first + second step: ", time3, 's')
                json["time elapsed during first + second step"] = time3
                
                println(fout)
                
                
                println(fout, "Z: ", Z)
                json["Z"] = Z
                
                println(fout, "total throuput before the second step:", sum(values(demand)) / max(Z, 1))
                json["total throuput before the second step"] = sum(values(demand)) / max(Z, 1)
                
                total_throuput = sum(d / Zs[pair] for (pair, d) in demand)
                println(fout, "total throuput after the second step:", total_throuput)
                json["total throuput after the second step"] = total_throuput
                
                println(fout)
                
                
                println(fout, "number of path through each node:")
                json["number of path through each node"] = x = Dict()
                
                node_dict = Dict(n => 0 for n in nodes)
                for (pair, paths) in m2_scheme, (path, weight) in paths, edge in path
                    n = split(edge, ' ') |> car
                    if car(n) == 's'
                        node_dict[n] += 1
                    end
                end
                for (node, number) in sort(collect(node_dict), lt=natural, by=car)
                    println(fout, "  ", node, ": ", number)
                    x[node] = number
                end
                
                println(fout, "  average: ", sum(values(node_dict)) / length(node_dict))
                x["average"] = sum(values(node_dict)) / length(node_dict)
                
                println(fout)
                
                
                println(fout, "number of path, total flow, and link utiliaztion of each edge:")
                json["number of path, total flow, and link utiliaztion of each edge"] = x = Dict()
                
                edge_dict = Dict(e => f64[] for e in edges)
                for (pair, paths) in m2_scheme, (path, weight) in paths, edge in path @when 'h' ∉ edge
                    push!(edge_dict[edge], demand[pair] * weight / Zs[pair])
                end
                for (edge, flows) in sort(collect(edge_dict), lt=natural, by=car)
                    println(fout, "  ", edge, ": ", length(flows), ", ", sum(flows), ", ", sum(flows) / 10, '%')
                    x[edge] = [length(flows), sum(flows), sum(flows) / 10]
                end
                
                println(fout, "  average: ", sum(length(v) for v in values(edge_dict)) / length(edge_dict), 
                                       ", ", sum(sum(v) for v in values(edge_dict)) / length(edge_dict),
                                       ", ", sum(sum(v) for v in values(edge_dict)) / length(edge_dict) / 10, '%')
                x["average"] = [sum(length(v) for v in values(edge_dict)) / length(edge_dict),
                                sum(sum(v) for v in values(edge_dict)) / length(edge_dict),
                                sum(sum(v) for v in values(edge_dict)) / length(edge_dict) / 10]
                
                println(fout)
                
                
                println(fout, "number of path and demand ratio of each st pair:")
                json["number of path and demand ratio of each st pair"] = x = Dict()
                
                pair_dict = Dict(pair => length(paths) for (pair, paths) in m2_scheme)
                for (pair, nflows) in sort(collect(pair_dict), lt=natural, by=car)
                    println(fout, "  ", pair, ": ", nflows, ", ", 1 / Zs[pair] * 100, '%')
                    x[pair] = [nflows, 1 / Zs[pair] * 100]
                end
                println(fout, "  average: ", sum(values(pair_dict)) / length(pair_dict),
                                       ", ", sum(d / Zs[pair] for (pair, d) in demand) / sum(values(demand)) * 100, '%')
                x["average"] = [sum(values(pair_dict)) / length(pair_dict),
                                sum(d / Zs[pair] for (pair, d) in demand) / sum(values(demand)) * 100]
                
                println(fout)

                println(fout, "Z, total throuput, and throuput ratio at single edge failure:")
                json["Z, total throuput, and throuput ratio at single edge failure"] = x = Dict()
                                                                        
                edge_dict = single_failure(nodes, edges, demand, raw_scheme)
                for (edge, res) in sort(collect(edge_dict), lt=natural, by=car)
                    if res isa String
                        println(fout, "  ", edge, ": ", res)
                        x[edge] = res
                    else
                        Z, tt = res
                        println(fout, "  ", edge, ": ", Z, ", ", tt, ", ", tt / total_throuput * 100, '%')
                        x[edge] = Z, tt, tt / total_throuput * 100
                    end
                end
                for r in (90, 95, 99, 99.9, 99.99)
                    println(fout, "  P(T > $r%): ", mean(p isa Tuple && p[3] >= r for (e, p) in x if !startswith(e, 'P')))
                    x["P(T > $r%)"] = mean(p isa Tuple && p[3] >= r for (e, p) in x if !startswith(e, 'P'))
                end
                println(fout)

                                                                        
                println(fout, "path set:")
                json["path set"] = x = Dict()
                write_scheme(fout, path_sets[algo], x)
                println(fout)
                
                println(fout, "paths selected:")
                json["paths selected"] = x = Dict()
                write_scheme(fout, raw_scheme, x)
                println(fout)
                
                println(fout, "paths after the first step (minimize maximum link utilization):")
                json["paths after the first step (minimize maximum link utilization)"] = x = Dict()
                write_scheme(fout, m1_scheme, x)
                println(fout)
                
                println(fout, "paths after the second step (maximize total throuput):")
                json["paths after the second step (maximize total throuput)"] = x = Dict()
                write_scheme(fout, m2_scheme, x)
            end
            
            open("results/$data-$i-$algo-$name.json", "w") do fout
                JSON.print(fout, json, 2)
            end
        end
    end
end
