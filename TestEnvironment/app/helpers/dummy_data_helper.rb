module DummyDataHelper
  require 'json'

  def get_dummy_cluster
    data = File.read(Rails.root.join("public/json_files/dummy_cluster.json"))

    return data
  end

  def get_dummy_data_set
    data = File.read(Rails.root.join('public/json_files/dummy_data_set.json'))

    return data
  end

  def get_dummy_simulation
    data = File.read(Rails.root.join('public/json_files/dummy_simulation.json'))

    return data
  end
end
