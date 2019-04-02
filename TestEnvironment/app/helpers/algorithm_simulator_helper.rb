module AlgorithmSimulatorHelper

  require 'open3'
  require 'expect'
  require 'io/wait'

  def run_simulation_script(info_cluster, info_jobs, script_path)

    puts script_path
    # Open3.popen3(['python', File.expand_path('../LoadBalancing/simulator.py')], mode='rw+') do  |stdin, stdout, stderr|
    #   stdout.close_write
    # end

=begin
    IO.popen(['python', script_path], mode='r+') do |pipe|
      pipe.puts info_cluster
      pipe.close_write

      result_cluster = pipe.gets

      puts result_cluster

      pipe.puts info_jobs
      pipe.close_write

      result_jobs = pipe.gets


      puts result_jobs

    end
=end

    Open3.popen3(['python', script_path]) do |stdin, stdout, stderr|

      stdin.puts info_cluster

      while line =  stdout.gets
        puts line
      end

      stdin.puts info_jobs
=begin
      result_jobs = stdout.read

      puts result_jobs
=end
    end


=begin
    slave = IO.popen(['python', script_path], mode = 'r+')

    # slave.write info_cluster
    slave.puts info_cluster
    slave.clo

    line = slave.readline
    puts line

    slave.write info_jobs
    slave.close_write

    line = slave.readline
    puts line
=end

=begin
    Open3.popen3(['python', script_path]) do | input, output, error, wait_thr|
      input.sync = true
      output.sync = true

      input.write info_cluster

      while output.ready?
        puts output.readline
      end
      # puts output.expect("OK1", 4)

      input.write info_jobs
      while output.ready?
        puts output.readline
      end
      # puts output.expect("OK2", 4)

    end
=end

=begin
    stdin, stdout, stderr = Open3.popen3(['python', script_path])

    stdin.puts info_cluster

    puts "1"

    while stdout.ready?
      puts stdout.readline
    end

    puts "2"

    stdin.puts info_jobs

    puts "3"

    while stdout.ready?
      puts stdout.readline
    end

    puts "4"
=end

=begin
    Open3.popen3("sleep 2; ls") do |stdout, stderr, status, thread|
      while line=stderr.gets do
        puts(line)
      end
    end
=end


  end

end
