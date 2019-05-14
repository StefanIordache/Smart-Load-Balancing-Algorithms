class AddAlgorithmToSimulation < ActiveRecord::Migration[5.2]
  def change
    add_column :simulations, :algorithm, :string
  end
end
