module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(info_cluster, info_jobs, script_path)

=begin
    simulator = IO.popen(['python', script_path], mode = 'r+')

    simulator.puts info_cluster

    line = simulator.readline
    puts line

    simulator.puts info_jobs

    line = simulator.readline
    puts line
=end

    server = TCPServer.new 3001

      Thread.start(server.accept) do |client|

        client.puts info_cluster
        client.flush

        line = client.recv(1024)
        puts line

        client.puts info_jobs
        client.flush

        line = client.recv(1024)
        puts line

        client.close
        break
      end

    server.close

  end

end
