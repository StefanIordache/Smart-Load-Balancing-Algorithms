Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root :to => "home#index"

  get 'algorithm_simulator', to: 'algorithm_simulator#index'
  post 'simulate', to: 'algorithm_simulator#simulate'

  get 'dummy/cluster', to: 'dummy_data#cluster'
  get 'dummy/data_set', to: 'dummy_data#data_set'
  get 'dummy/simulation', to: 'dummy_data#simulation'

  get 'templates', to: 'templates#index'


  get 'request/get_snapshots_counter_by_simulation_id', to: 'request#get_snapshots_counter_by_simulation_id'
  get 'request/get_snapshots_json_by_simulation_id_and_index', to: 'request#get_snapshots_json_by_simulation_id_and_index'


  get 'data_sets', to: 'data_sets#index'
  get 'data_sets/get_all_data_sets', to: 'data_sets#get_all_data_sets'
  get 'data_sets/data_set', to: 'data_sets#get_data_set'
  get 'data_sets/check_if_data_set_name_is_used', to: 'data_sets#check_if_data_set_name_is_used'
  post 'data_sets/delete_data_set', to: 'data_sets#delete_data_set'

  post 'create_new_data_set', to: 'data_sets#create_new_data_set'

end
