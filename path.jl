const Scheme = Dict{String, Vector{Tuple{Vector{String}, Float64}}}

function parse_schemes(io)
    results = Dict{String, Scheme}()
    
    calgo, cpair = nothing, nothing
    for line in eachline(io) @when !isempty(line)
        if (m = match(r"\*\*\*(.*)\*\*\*", line)) != nothing
            results[m[1]] = Scheme()
            calgo = results[m[1]]
        elseif (m = match(r"(.*) -> (.*) :", line)) != nothing
            if m[1] != m[2]
                calgo["$(m[1]) $(m[2])"] = []
                cpair = calgo["$(m[1]) $(m[2])"]
            else
                cpair = nothing
            end
        elseif cpair != nothing
            path, weight = split(line, '@')
            weight = parse(f64, weight)
            path = [join(edge.args, ' ') for edge in parse(path).args]
            push!(cpair, (path, weight))
        end
    end
    
    results
end

function renormalize(scheme)
    map(scheme) do p
        pair, paths = p
        tw = sum(cadr, paths)
        pair => [(path, weight / tw) for (path, weight) in paths]
    end
end

function renormalize!(scheme, pair)
    paths = scheme[pair]
    tw = sum(cadr, paths)
    scheme[pair] = [(path, weight / tw) for (path, weight) in paths]
end

function select_hard_nop(nodes, edges, scheme, budget)
    function meet_budget()
        d = Dict(n => 0 for n in nodes)
        for (pair, paths) in scheme, (path, weight) in paths, edge in path
            n = split(edge, ' ') |> car
            if car(n) == 's'
                d[n] += 1
            end
        end
        all(x <= budget[n] for (n, x) in d)
    end
                
    function cut_down(K)
        Dict(pair => length(paths) > K ? sort(paths, by=cadr, rev=true)[1:K] : paths for (pair, paths) in scheme)
    end

    K = maximum(map(length, collect(values(scheme))))
                
    while !meet_budget() && K > 0
        scheme = cut_down(K)
        K -= 1
    end
    
    renormalize(scheme)
end

function select_greedy(nodes, edges, scheme, budget)
    scheme = deepcopy(scheme)
    
    function dispute_one()
        d = Dict(n => [] for n in nodes)
        for (pair, paths) in scheme, (i, (path, weight)) in enumerate(paths), edge in path
            n = split(edge, ' ') |> car
            if car(n) == 's'
                push!(d[n], (pair, i, weight))
            end
        end
        
        overloads = Set()
        for (n, v) in d @when length(v) > budget[n]
            push!(overloads, v...)
        end
        
        if length(overloads) > 0
            pair, i, w = min(overloads..., by=i"3")
            deleteat!(scheme[pair], i)
            renormalize!(scheme, pair)
            true
        else
            false
        end
    end
    
    while dispute_one() end
    scheme
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
            m[:addConstr](py"sum($passed) <= $(budget[n])", name="n_$n")
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
            m[:addConstr](py"sum($passed) <= $(budget[n])", name="n_$n")
        end
    end
    
    all_paths = [v for l in values(pathvar) for v in l]
    
    m[:setObjective](py"sum($all_paths)", sense=grb.GRB[:MAXIMIZE])
    m[:optimize]()
                
    Dict(pair => [path for (path, choice) in zip(paths, pathvar[pair]) if choice[:X] > .5]
         for (pair, paths) in scheme)
end