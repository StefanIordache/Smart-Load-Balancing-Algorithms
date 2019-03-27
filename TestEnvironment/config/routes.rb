Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root :to => "home#index"

  get 'algorithm_simulator', to: 'algorithm_simulator#index'
  post 'simulate', to: 'algorithm_simulator#simulate'

  get 'dummy/cluster', to: 'dummy_data#cluster'
  get 'dummy/jobs', to: 'dummy_data#jobs'

  get 'templates', to: 'templates#index'

end
