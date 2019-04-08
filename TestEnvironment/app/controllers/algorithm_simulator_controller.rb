class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  include AlgorithmSimulatorHelper

  def index
  end

  def simulate
    info_cluster = params[:payload_cluster].to_json
    info_jobs = params[:payload_jobs].to_json

    # File.expand_path('../LoadBalancing/simulator.py')

    run_simulation_script info_cluster, info_jobs

  end
end
