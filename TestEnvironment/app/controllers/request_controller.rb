require 'json'

class RequestController < ApplicationController

  include RequestHelper

  def get_snapshots_counter_by_simulation_id
    if params[:simulation_id].present?
      simulation = Simulation.find(params[:simulation_id])

      snapshots_counter = count_simulation_snapshots(simulation.storage_path)

      render json: snapshots_counter.to_json
    else
      render json: ""
    end
  end

  def get_snapshots_json_by_simulation_id_and_index

    if params[:simulation_id].present? and params[:index].present?
      simulation = Simulation.find(params[:simulation_id])

      snapshots = get_snapshots_from_file(simulation.storage_path, params[:index])

      render json: snapshots
    else
      render json: ""
    end
  end


end
