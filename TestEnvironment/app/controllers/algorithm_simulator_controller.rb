class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  include AlgorithmSimulatorHelper

  def index

    @algorithms = %w(FCFS Round-Robin MCT)

  end

  def simulate
    info_cluster = params[:payload_cluster].to_json
    info_jobs = params[:payload_jobs].to_json
    simulated_algorithm = params[:simulated_algorithm]

    simulation = Simulation.new(algorithm: simulated_algorithm, cluster_params: info_cluster, jobs_params: info_jobs, storage_path: "")
    simulation.save

    run_simulation_script simulation, info_cluster, info_jobs, simulated_algorithm

  end
end
