Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root :to => "home#index"

  get 'test', to: 'test#index'
  post 'simulate', to: 'test#simulate'

  get 'dummy/systems', to: 'dummy_data#systems'

  get 'templates', to: 'templates#index'

end
