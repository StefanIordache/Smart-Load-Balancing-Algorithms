module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(info_cluster, info_jobs, script_path)

    puts script_path

    slave = IO.popen(['python', script_path], mode = 'r+')

    slave.puts info_cluster

    line = slave.readline
    puts line

    slave.puts info_jobs

    line = slave.readline
    puts line


  end

end
