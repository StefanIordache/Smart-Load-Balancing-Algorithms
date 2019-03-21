class CreateTemplates < ActiveRecord::Migration[5.2]
  def change
    create_table :templates do |t|
      t.string :title
      t.string :description
      t.json :parameters

      t.timestamps
    end
  end
end
