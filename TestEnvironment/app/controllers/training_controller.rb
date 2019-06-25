class TrainingController < ApplicationController
  protect_from_forgery with: :null_session

  include TrainingHelper

  def index

  end

end
