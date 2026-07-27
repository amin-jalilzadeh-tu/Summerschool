using JuMP, HiGHS, CSV
import MultiObjectiveAlgorithms as MOA

struct Configuration
    id::String
    pv::Int64
    daylight::Int64
    compactness::Int64
    fsi::Int64
end

function non_dominated_configurations(configs::AbstractVector{Configuration})
    return filter(configs) do config
        !any(
            other -> other.id != config.id &&
                     other.pv >= config.pv &&
                     other.daylight >= config.daylight &&
                     other.compactness >= config.compactness &&
                     other.fsi >= config.fsi &&
                     (other.pv > config.pv ||
                      other.daylight > config.daylight ||
                      other.compactness > config.compactness ||
                      other.fsi > config.fsi),
            configs
        )
    end
end

configurationsCSV = CSV.File(joinpath(@__DIR__, "..", "data", "configurations.csv"))

configurations = Dict{String, Configuration}()
for row in configurationsCSV
    config = Configuration(row.id, round(Int, row.pv * 100), round(Int, row.daylight * 100), round(Int, row.compactness * 100), round(Int, row.fsi * 100))
    configurations[config.id] = config
end

MIN_PV = 70
MIN_FSI = 80
MIN_DAYLIGHT = 70
MIN_COMPACTNESS = 75

candidate_configs = collect(values(configurations))
candidate_configs = filter(
    config -> config.pv >= MIN_PV && config.fsi >= MIN_FSI && config.daylight >= MIN_DAYLIGHT && config.compactness >= MIN_COMPACTNESS,
    candidate_configs
)
# candidate_configs = non_dominated_configurations(candidate_configs)

configurations = Dict{String, Configuration}(config.id => config for config in candidate_configs)

display(configurations)
N = length(configurations)

model = Model(() -> MOA.Optimizer(HiGHS.Optimizer))
@variable(model, x[keys(configurations)], Bin)

@constraint(model, cons_at_most_one, sum(x) == 1) # Only one configuration can be selected

# removing non feasible soltions based on minimum requirements
@constraint(model, cons_min_pv[i in keys(configurations)], x[i] * MIN_PV <= configurations[i].pv)
@constraint(model, cons_min_fsi[i in keys(configurations)], x[i] * MIN_FSI <= configurations[i].fsi)
@constraint(model, cons_min_daylight[i in keys(configurations)], x[i] * MIN_DAYLIGHT <= configurations[i].daylight)
@constraint(model, cons_min_compactness[i in keys(configurations)], x[i] * MIN_COMPACTNESS <= configurations[i].compactness)

# making the objectives
@expression(model, total_pv, sum(configurations[i].pv * x[i] for i in keys(configurations)))
@expression(model, total_fsi, sum(configurations[i].fsi * x[i] for i in keys(configurations)))
@expression(model, total_daylight, sum(configurations[i].daylight * x[i] for i in keys(configurations)))
@expression(model, total_compactness, sum(configurations[i].compactness * x[i] for i in keys(configurations)))

# Adding the objectives to the model
# @objective(model, Max, [total_pv, total_fsi, total_daylight, total_compactness])
@objective(model, Min, [total_pv, total_daylight, total_compactness, total_fsi])

# set_attribute(model, MOA.Algorithm(), MOA.Lexicographic())
set_attribute(model, MOA.Algorithm(), MOA.KirlikSayin())

# for id in keys(configurations)
#     fix(x[id], id == "C28" ? 1 : 0, force=true)
# end

optimize!(model)

if is_solved_and_feasible(model)
    println("Pareto front found with $(result_count(model)) solutions.")
    for i in 1:result_count(model)
        objs = objective_value(model, result = i) 
        println("Solution $i:")
        println("\tObjective values: ", objs ./ 100)
        for v in all_variables(model)
            if value(v; result=i) > 0.5
                println("\t$v = ", value(v; result=i))
            end
        end
    end
else
    println("No feasible solution found.")
end



