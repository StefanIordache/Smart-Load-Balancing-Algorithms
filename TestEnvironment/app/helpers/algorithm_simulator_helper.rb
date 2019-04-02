module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(info_cluster, info_jobs, script_path)

    simulator = IO.popen(['python', script_path], mode = 'r+')

    simulator.puts info_cluster

    line = simulator.readline
    puts line

    simulator.puts info_jobs

    line = simulator.readline
    puts line

    server = TCPServer.new 5163

    loop do
      Thread.start(server.accept) do |client|

        client.puts info_cluster

        line = server.readline
        puts line

        client.puts info_jobs

        line = server.readline
        puts line

        client.close
      end
    end

    server.close

  end

end
