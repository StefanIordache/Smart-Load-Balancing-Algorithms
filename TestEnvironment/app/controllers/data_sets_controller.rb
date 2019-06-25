class DataSetsController < ApplicationController
  protect_from_forgery with: :null_session

  include DataSetsHelper

  def index

  end

  def create_new_data_set
    info_data_set = params[:payload_data_set].to_json
    data_set_name = params[:payload_data_set_name]

    puts data_set_name

    data_set = DataSet.new(raw_json: info_data_set, name: data_set_name)
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

  def get_all_data_sets
    render json: { data: DataSet.all }
  end

  def delete_data_set
    puts params

    if params[:data_set_id].present?
      DataSet.destroy(params[:data_set_id])

      render json: true
    end
  end

  def get_data_set

    puts params
    if params[:data_set_id].present?
      data_set = DataSet.find(params[:data_set_id])

      render json: data_set
    else
      render json: ""
    end

  end

  def check_if_data_set_name_is_used
    puts params

    if params[:data_set_name].present?
      name_already_exists = true
      data_sets = DataSet.where(name: params[:data_set_name])

      if data_sets.empty?
        name_already_exists = false
      end

      render json: name_already_exists
    end
  end

end
