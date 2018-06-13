const ϵ = 1e-6

function minimize_maximum_link_utilization(nodes, edges, demand, scheme)
    m = grb.Model("Z")
    m[:setParam]("OutputFlag", false)
    
    Z = m[:addVar](name="Z")
    
    weights, passed = Dict(), Dict(n => [] for n in nodes)
    for (pair, paths) in scheme
        weights[pair] = map(enumerate(paths)) do p
            i, (path, weight) = p
            x = m[:addVar]()
            for edge in path
                n = split(edge, ' ') |> car
                if car(n) == 's'
                    push!(passed[n], demand[pair] * x)
                end
            end
            x
        end
    end
    m[:update]()
    
    # constraint 1: weights adds to 1
    for (pair, w) in weights
        m[:addConstr](py"sum($w) == 1")
    end
    
    # constraint 2: do not exceed capacity * Z
    for (n, v) in passed
        m[:addConstr](py"sum($v) <= 1000 * $Z")
    end
    
    m[:setObjective](Z)
    m[:optimize]()
    
    newscheme = Dict(pair => [(path, v[:X]) for ((path, weight), v) in zip(paths, weights[pair])]
                     for (pair, paths) in scheme)

    newscheme, Z[:X]
end

function minimize_maximum_link_utilization_then_maximize_throuput(nodes, edges, demand, scheme)
    scheme, Z = minimize_maximum_link_utilization(nodes, edges, demand, scheme)
    
    Z <= 1 && return scheme, sum(values(demand))
    
    m = grb.Model("throuput")
    m[:setParam]("OutputFlag", false)
    
    bandwidths, passed = Dict(), Dict(n => [] for n in nodes)
    for (pair, paths) in scheme
        bandwidths[pair] = map(enumerate(paths)) do p
            i, (path, bandwidth) = p
            x = m[:addVar]()
            for edge in path
                n = split(edge, ' ') |> car
                if car(n) == 's'
                    push!(passed[n], x)
                end
            end
            x
        end
    end
    m[:update]()
    
    # constraint 1: d/Z ⩽ ∑b ⩽ d
    for (pair, b) in bandwidths
        m[:addConstr](py"sum($b) <= $(demand[pair])")
        m[:addConstr](py"sum($b) >= $(demand[pair] / (Z + ϵ))")
    end
    
    # constraint 2: do not exceed capacity
    for (n, v) in passed
        m[:addConstr](py"sum($v) <= 1000")
    end
    
    total_flow = [b for l in values(bandwidths) for b in l]
    m[:setObjective](py"sum($total_flow)", sense=grb.GRB[:MAXIMIZE])
    m[:optimize]()
                
    newscheme, total_flow = Dict(), 0
    for (pair, paths) in scheme
        tb = sum(i":X", bandwidths[pair])
        newscheme[pair] = [(path, b[:X] / tb) for ((path, _), b) in zip(paths, bandwidths[pair])]
        total_flow += tb
    end
    newscheme, total_flow
end

