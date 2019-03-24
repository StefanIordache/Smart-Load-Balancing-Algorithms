module DummyDataHelper
  require 'json'

  def get_dummy_systems_json
    data = File.read(Rails.root.join("public/json_files/dummy_system_setup.json"))

    return data
  end
end
