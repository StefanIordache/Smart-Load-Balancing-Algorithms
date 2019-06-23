module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_simulation_script(simulation, info_cluster, info_simulation, algorithm, data_set_id)
    simulation_completed_with_success = false

    begin
      pid = Process.spawn "bash " + File.expand_path('../Scripts/simulator.sh')

      finished_with_success = false
      storage_path = ""

      server = TCPServer.new 3001

      computation = Thread.start(server.accept) do |client|

        client.puts String(simulation.id_before_type_cast)
        client.flush

        sleep 0.1

        client.puts info_cluster
        client.flush

        sleep 0.1

        client.puts info_simulation
        client.flush

        sleep 0.1

        client.puts algorithm
        client.flush

        sleep 0.1

        client.puts String(data_set_id)
        client.flush

        finished = client.recv(1024)
        puts finished

        errors = client.recv(1024)
        puts errors

        if errors == 'NO ERRORS' && finished == 'FINISHED'
          finished_with_success = true
        end

        client.close

      end

      computation.join

      server.close

      if finished_with_success == true
        simulation_completed_with_success = true
      else
        simulation.destroy
      end

    rescue LocalJumpError
    rescue
    end

    return simulation_completed_with_success

  end

end
