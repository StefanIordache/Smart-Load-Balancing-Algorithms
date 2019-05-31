module RequestHelper

  def count_simulation_snapshots(storage_path)
    app_storage_base_path = "app/storage/simulations/"

    directory_path = File.join(Rails.root.join(app_storage_base_path + storage_path + "/snapshots"), "**", "*")

    count = Dir.glob(directory_path).count

    return count
  end

  def get_snapshots_from_file(storage_path, file_index)
    app_storage_base_path = "app/storage/simulations/"

    data = File.read(Rails.root.join(app_storage_base_path + storage_path + "/snapshots/" + file_index.to_s + ".json"))

    return data
  end

end
