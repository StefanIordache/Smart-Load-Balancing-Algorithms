module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(simulation, info_cluster, info_jobs, simulated_algorithm)

    begin
      pid = Process.spawn "bash " + File.expand_path('../Scripts/simulator.sh')

      finished_with_success = false
      storage_path = ""

      server = TCPServer.new 3001

      computation = Thread.start(server.accept) do |client|

        client.puts String(simulation.id_before_type_cast)
        client.flush

        sleep 0.1

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

        finished = client.recv(1024)
        puts finished

        errors = client.recv(1024)
        puts errors

        storage_path = client.recv(1024)
        puts storage_path

        if errors == 'NO ERRORS' && finished == 'FINISHED'
          finished_with_success = true
        end

        client.close

      end

      computation.join

      server.close

      if finished_with_success == true
        simulation.update(storage_path: storage_path.reverse.chomp('../Storage/').reverse)
      else
        simulation.destroy
      end

    rescue LocalJumpError
      puts "salvarea"
    rescue
      puts "ultima salvare"
    end

  end

end
