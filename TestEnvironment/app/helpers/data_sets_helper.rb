module DataSetsHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_data_set_generator(data_set)
    data_set_generated_with_success = false

    begin
      pid = Process.spawn "bash " + File.expand_path('../Scripts/data_set_generator.sh')

      finished_with_success = false
      storage_path = ""

      server = TCPServer.new 3001

      computation = Thread.start(server.accept) do |client|

        client.puts String(data_set.id_before_type_cast)
        client.flush

        sleep 0.1

        client.puts data_set.raw_json
        client.flush

        finished = client.recv(1024)
        puts finished

        errors = client.recv(1024)
        puts errors

        if errors == 'NO ERRORS' && finished == 'FINISHED'
          finished_with_success = true

          storage_path = client.recv(1024)
          puts storage_path
        end

        client.close

      end

      computation.join

      server.close

      if finished_with_success == true
        data_set.update(storage_path: storage_path.reverse.chomp('../Storage/').reverse)
        data_set_generated_with_success = true
      else
        data_set.destroy
      end

    rescue LocalJumpError
    rescue
    end

    return data_set_generated_with_success

  end

end
