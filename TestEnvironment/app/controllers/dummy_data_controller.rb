class DummyDataController < ApplicationController

  include DummyDataHelper

  def cluster
    render json: get_dummy_cluster
  end

  def data_set
    render json: get_dummy_data_set
  end

  def simulation
    render json: get_dummy_simulation
  end

end
