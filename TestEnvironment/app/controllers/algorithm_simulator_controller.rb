class AlgorithmSimulatorController < ApplicationController
  protect_from_forgery with: :null_session

  def index
  end

  def simulate
    info_cluster = params[:payload_cluster]
    info_jobs = params[:payload_jobs]

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
