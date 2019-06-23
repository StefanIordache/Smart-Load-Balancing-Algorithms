class RemoveStoragePathFromSimulations < ActiveRecord::Migration[5.2]
  def change
    remove_column :simulations, :storage_path, :string
  end
end
