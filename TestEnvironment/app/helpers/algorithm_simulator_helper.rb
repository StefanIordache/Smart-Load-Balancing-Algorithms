module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(info_cluster, info_jobs, simulated_algorithm)

    begin
      pid = Process.spawn "bash " + File.expand_path('../Scripts/simulator.sh')

      server = TCPServer.new 3001

      computation = Thread.start(server.accept) do |client|

        client.puts simulated_algorithm
        client.flush

        line = client.recv(1024)
        puts line

        client.puts info_cluster
        client.flush

        line = client.recv(1024)
        puts line

        client.puts info_jobs
        client.flush

        line = client.recv(1024)
        puts line

        line = client.recv(1024)
        puts line

        line = client.recv(1024)
        puts line

        client.close

      end

      computation.join

      server.close
    rescue LocalJumpError
      puts "salvarea"
    rescue
      puts "ultima salvare"
    end

  end

end
