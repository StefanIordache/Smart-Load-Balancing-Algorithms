class AddJobsParamsToSimulation < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :jobs_params, :json
  end
end
