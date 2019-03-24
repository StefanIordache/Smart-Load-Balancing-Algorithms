class TestController < ApplicationController

    protect_from_forgery with: :null_session

    def index

    end

    def simulate
        logger.info params[:payload]
        raise "baaam"
    end

end
