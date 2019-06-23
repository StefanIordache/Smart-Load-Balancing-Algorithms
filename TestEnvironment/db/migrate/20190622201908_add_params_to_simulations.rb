class AddParamsToSimulations < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :params, :json
  end
end
