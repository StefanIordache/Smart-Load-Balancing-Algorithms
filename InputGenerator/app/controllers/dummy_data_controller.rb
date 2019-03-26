class DummyDataController < ApplicationController

  include DummyDataHelper

  def cluster
    render json: get_dummy_cluster_json
  end

  def jobs
    render json: get_dummy_jobs_json
  end

end
