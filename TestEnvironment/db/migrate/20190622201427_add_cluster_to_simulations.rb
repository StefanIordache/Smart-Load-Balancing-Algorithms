class AddClusterToSimulations < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :cluster, :json
  end
end
