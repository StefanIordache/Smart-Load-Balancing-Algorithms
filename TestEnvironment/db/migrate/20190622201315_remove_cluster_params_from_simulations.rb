class RemoveClusterParamsFromSimulations < ActiveRecord::Migration[5.2]
  def change
    remove_column :simulations, :cluster_params, :json
  end
end
