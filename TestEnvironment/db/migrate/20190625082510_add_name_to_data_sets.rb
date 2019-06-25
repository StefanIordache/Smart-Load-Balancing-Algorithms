class AddNameToDataSets < ActiveRecord::Migration[5.2]
  def change
    add_column :data_sets, :name, :string
  end
end
