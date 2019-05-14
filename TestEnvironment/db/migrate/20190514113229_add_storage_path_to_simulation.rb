class AddStoragePathToSimulation < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :storage_path, :string
  end
end
