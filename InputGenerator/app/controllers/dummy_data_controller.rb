class DummyDataController < ApplicationController

  include DummyDataHelper

  def systems
    render json: get_dummy_systems_json
  end

end
