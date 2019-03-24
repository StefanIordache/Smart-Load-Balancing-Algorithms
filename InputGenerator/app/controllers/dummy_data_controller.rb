class DummyDataController < ApplicationController

  include DummyDataHelper

  def cluster
    render json: get_dummy_cluster_json
  end

end
