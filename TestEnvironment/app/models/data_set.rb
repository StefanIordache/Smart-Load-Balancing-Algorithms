class DataSet < ApplicationRecord

  def created_at
    attributes['created_at'].strftime("%m/%d/%Y %H:%M:%S")
  end

  has_many :simulations
end
