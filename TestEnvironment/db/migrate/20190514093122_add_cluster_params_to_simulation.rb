class AddClusterParamsToSimulation < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :cluster_params, :json
  end
end
