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

    run_simulation_script info_cluster, info_jobs, simulated_algorithm

  end
end
