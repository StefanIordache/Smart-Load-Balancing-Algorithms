class AddDataSetIdToSimulations < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :data_set_id, :integer
    add_index  :simulations, :data_set_id
  end
end
