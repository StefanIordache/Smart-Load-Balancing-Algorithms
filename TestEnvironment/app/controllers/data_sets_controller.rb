class DataSetsController < ApplicationController
  protect_from_forgery with: :null_session

  include DataSetsHelper

  def index

  end

  def create_new_data_set
    info_data_set = params[:payload_data_set].to_json

    data_set = DataSet.new(raw_json: info_data_set)
    data_set.save

    data_set_generated_with_success = run_data_set_generator data_set

    result = OpenStruct.new

    if data_set_generated_with_success == false
      result.status = "failed"
    else
      result.status = "successful"
      result.data_set = data_set
    end

    render json: result.to_json

  end
end
