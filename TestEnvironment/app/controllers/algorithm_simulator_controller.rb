class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  include AlgorithmSimulatorHelper

  def index

    @algorithms = %w(FCFS PARALLELIZED-FCFS OPTIMIZED-FCFS MCT MET)

  end

  def simulate
    info_cluster = params[:payload_cluster].to_json
    info_jobs = params[:payload_jobs].to_json
    simulated_algorithm = params[:simulated_algorithm]

    simulation = Simulation.new(algorithm: simulated_algorithm, cluster_params: info_cluster, jobs_params: info_jobs, storage_path: "")
    simulation.save

    simulation_completed_with_success = run_simulation_script simulation, info_cluster, info_jobs, simulated_algorithm

    result = OpenStruct.new

    if simulation_completed_with_success == false
      result.status = "failed"
    else
      result.status = "successful"
      result.simulation = simulation
    end

    render json: result.to_json

  end
end
