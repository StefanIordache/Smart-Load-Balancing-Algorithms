module TrainingHelper

  require 'open3'
  require 'expect'
  require 'io/wait'
  require 'io/console'
  require 'socket'

  def run_training(training_type, data_set_id, number_of_epochs, output_file_format, output_frequency)

    puts training_type
    puts data_set_id
    puts number_of_epochs
    puts output_file_format
    puts output_frequency

    begin
      pid = Process.spawn "bash " + File.expand_path('../Scripts/training.sh') + " " +
          training_type.downcase + " " + data_set_id + " " + number_of_epochs + " " + output_file_format + " " + output_frequency

    rescue LocalJumpError
    rescue
    end

  end

end
