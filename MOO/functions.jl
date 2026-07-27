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


function solve_problem(configs::Vector{Configuration}, MIN_PV::Int, MIN_FSI::Int, MIN_DAYLIGHT::Int, MIN_COMPACTNESS::Int; verbose::Bool=false)
    # This function will be implemented later
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
    @objective(model, Max, [total_pv, total_daylight, total_compactness, total_fsi])

    # set_attribute(model, MOA.Algorithm(), MOA.Lexicographic())
    set_attribute(model, MOA.Algorithm(), MOA.KirlikSayin())
    set_silent(model)
    optimize!(model)

    if is_solved_and_feasible(model)
        sol = []
        verbose && println("Pareto front found with $(result_count(model)) solutions.")
        for i in 1:result_count(model)
            objs = objective_value(model, result = i) 
            verbose && println("Solution $i:")
            verbose && println("\tObjective values: ", objs ./ 100)
            for v in all_variables(model)
                if value(v; result=i) > 0.5
                    verbose && println("\t$v = ", value(v; result=i))
                    push!(sol, name(v))
                end
            end
        end
        return sol
    else
        verbose && println("No feasible solution found.")
    end
end

