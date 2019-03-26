module DummyDataHelper
  require 'json'

  def get_dummy_cluster_json
    data = File.read(Rails.root.join("public/json_files/dummy_cluster_setup.json"))

    return data
  end

  def get_dummy_jobs_json
    data = File.read(Rails.root.join("public/json_files/dummy_jobs.json"))

    return data
  end
end
