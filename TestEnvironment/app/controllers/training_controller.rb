class TrainingController < ApplicationController
  protect_from_forgery with: :null_session

  include TrainingHelper

  def index

    @data_sets = DataSet.pluck(:name, :id)

  end


  def start_training
    selected_training_type = params[:selected_training_type]
    selected_data_set = params[:selected_data_set]
    number_of_epochs = params[:number_of_epochs]
    output_file_format = params[:output_file_format]
    output_frequency = params[:output_frequency]

    run_training(selected_training_type, selected_data_set, number_of_epochs, output_file_format, output_frequency)

    render json: "FINISHED TRAINING"
  end

end
