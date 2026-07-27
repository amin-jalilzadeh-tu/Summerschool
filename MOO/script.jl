include("functions.jl")


configurationsCSV = CSV.File(joinpath(@__DIR__, "..", "data", "configurations.csv"))

configurations = Dict{String, Configuration}()
for row in configurationsCSV
    config = Configuration(row.id, round(Int, row.pv * 100), round(Int, row.daylight * 100), round(Int, row.compactness * 100), round(Int, row.fsi * 100))
    configurations[config.id] = config
end

candidate_configs = collect(values(configurations))

MIN_PVS = [70]
MIN_FSIS = [80]
MIN_DAYLIGHTS = [70]
MIN_COMPACTNESSES = [75, 90]

configurations = Dict{String, Configuration}(config.id => config for config in candidate_configs)

sols = []
for MIN_PV in MIN_PVS, MIN_FSI in MIN_FSIS, MIN_DAYLIGHT in MIN_DAYLIGHTS, MIN_COMPACTNESS in MIN_COMPACTNESSES
    sol = solve_problem(candidate_configs, MIN_PV, MIN_FSI, MIN_DAYLIGHT, MIN_COMPACTNESS)
    push!(sols, (sol=sol, MIN_PV=MIN_PV, MIN_FSI=MIN_FSI, MIN_DAYLIGHT=MIN_DAYLIGHT, MIN_COMPACTNESS=MIN_COMPACTNESS))
end

display(sols)