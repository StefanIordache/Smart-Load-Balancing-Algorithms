module AlgorithmSimulatorHelper

  require 'open3'

  def run_simulation_script(info_cluster, info_jobs, script_path)
    # Open3.popen3(['python', File.expand_path('../LoadBalancing/simulator.py')], mode='rw+') do  |stdin, stdout, stderr|
    #   stdout.close_write
    # end

=begin
    IO.popen(['python', script_path], mode='r+') do |pipe|
      pipe.puts info_cluster
      pipe.close_write

      result_cluster = pipe.gets

      pipe.puts info_jobs
      pipe.close_write

      result_jobs = pipe.gets

      puts result_cluster
      puts result_jobs
    end
=end

    Open3.popen3(['python', script_path]) do |stdin, stdout, stderr|
      stdin.puts info_cluster

      result_cluster = stdout.read

      stdin.puts info_jobs

      result_jobs = stdout.read

      stdin.close
      stdout.close

      puts result_cluster
      puts result_jobs
    end
  end

end
