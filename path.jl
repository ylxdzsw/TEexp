function renormalize(scheme)
    map(scheme) do p
        pair, paths = p
        tw = sum(cadr, paths)
        pair => [(path, weight / tw) for (path, weight) in paths]
    end
end

function select_program(nodes, edges, scheme, budget)
    # model 1: find K
    m = grb.Model("K")
    m[:setParam]("OutputFlag", false)
    K = m[:addVar](vtype=grb.GRB[:INTEGER], name="K")
    
    pathvar = Dict()
    for (pair, paths) in scheme
        p1, p2 = split(pair, ' ')
        pathvar[pair] = map(1:length(paths)) do i
            m[:addVar](vtype=grb.GRB[:BINARY], name="s_$(p1)_$(p2)_$(i)")
        end
    end
    m[:update]()
    
    # constraint 1: at least K paths
    for (pair, var) in pathvar
        p1, p2 = split(pair, ' ')
        m[:addConstr](py"sum($var) >= $K", name="d_$(p1)_$(p2)")
    end
    
    # constraint 2: flow table budget
    for n in nodes
        passed = []
        for (pair, paths) in scheme, (i, path) in enumerate(paths)
            for edge in car(path) @when n in split(edge, ' ')
                push!(passed, pathvar[pair][i])
                break
            end
        end
        if length(passed) > 0
            m[:addConstr](py"sum($passed) <= $budget", name="n_$n")
        end
    end
    
    m[:setObjective](K, sense=grb.GRB[:MAXIMIZE])
    m[:optimize]()
    
    K = K[:X]
    
    # model 2: maximize total number of paths
    m = grb.Model("totalnop")
    m[:setParam]("OutputFlag", false)
    
    pathvar = Dict()
    for (pair, paths) in scheme
        p1, p2 = split(pair, ' ')
        pathvar[pair] = map(1:length(paths)) do i
            m[:addVar](vtype=grb.GRB[:BINARY], name="s_$(p1)_$(p2)_$(i)")
        end
    end
    m[:update]()
    
    # constraint 1: at least K paths
    for (pair, var) in pathvar
        p1, p2 = split(pair, ' ')
        m[:addConstr](py"sum($var) >= $K", name="d_$(p1)_$(p2)")
    end
    
    # constraint 2: flow table budget
    for n in nodes
        passed = []
        for (pair, paths) in scheme, (i, path) in enumerate(paths)
            for edge in car(path) @when n in split(edge, ' ')
                push!(passed, pathvar[pair][i])
                break
            end
        end
        if length(passed) > 0
            m[:addConstr](py"sum($passed) <= $memory_budget", name="n_$n")
        end
    end
    
    all_paths = [v for l in values(pathvar) for v in l]
    
    m[:setObjective](py"sum($all_paths)", sense=grb.GRB[:MAXIMIZE])
    m[:optimize]()
                
    Dict(pair => [path for (path, choice) in zip(paths, pathvar[pair]) if choice[:X] > .5]
         for (pair, paths) in scheme)
end