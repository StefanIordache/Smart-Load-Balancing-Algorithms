class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  include AlgorithmSimulatorHelper

  def index

    @algorithms = %w(FCFS SJF)
    @data_sets = DataSet.pluck(:id)

  end

  def simulate
    info_cluster = params[:payload_cluster].to_json
    info_simulation = params[:payload_simulation].to_json
    algorithm = params[:simulated_algorithm]
    data_set_id = params[:data_set]

    data_set = DataSet.find(data_set_id)
    simulation = Simulation.new(algorithm: algorithm, cluster: info_cluster, params: info_simulation, data_set: data_set)
    simulation.save

    simulation_completed_with_success = run_simulation_script simulation, info_cluster, info_simulation, algorithm, data_set_id

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
