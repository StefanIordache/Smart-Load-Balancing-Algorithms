class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  include AlgorithmSimulatorHelper

  def index
  end

  def simulate
    info_cluster = params[:payload_cluster]
    info_jobs = params[:payload_jobs]

    run_simulation_script info_cluster, info_jobs, File.expand_path('../LoadBalancing/simulator.py')



=begin
    simulator = IO.popen(['python', File.expand_path('../LoadBalancing/simulator.py')], mode='r+')
    simulator.write info_cluster
    result_cluster = simulator.readline
    puts result_cluster
    if result_cluster == 'OK'
      simulator.write info_jobs
      result_jobs = simulator.readline
      logger.info(result_jobs)
      if result_jobs != 'OK'
        logger.info("jobs not ok")
      end
    else
      logger.info("cluster not ok")
    end
    simulator.close_read
=end




=begin
    (0..2).each do
      slave = IO.popen(['python', File.expand_path('../LoadBalancing/simulator.py')], mode = 'r+')
      slave.write "master"
      slave.close_write
      line = slave.readline
      while line do
        p eval line
        break if slave.eof
        line = slave.readline
      end
    end
=end
  end
end
