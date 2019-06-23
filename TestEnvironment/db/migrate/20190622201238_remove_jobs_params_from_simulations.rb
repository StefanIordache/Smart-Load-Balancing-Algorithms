class RemoveJobsParamsFromSimulations < ActiveRecord::Migration[5.2]
  def change
    remove_column :simulations, :jobs_params, :json
  end
end
