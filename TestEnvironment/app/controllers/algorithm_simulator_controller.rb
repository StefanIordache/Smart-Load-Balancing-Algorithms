class AlgorithmSimulatorController < ApplicationController
    protect_from_forgery with: :null_session

    def index

    end

    def simulate
        logger.info params[:payload]

        # (0..2).each do
        #     slave = IO.popen(['python', File.expand_path('../Test/slave.py')], mode='r+')
        #     slave.write "master"
        #     slave.close_write
        #     line = slave.readline
        #     while line do
        #       sleep 1
        #       p eval line
        #       break if slave.eof
        #       line = slave.readline
        #     end
        #   end

    end
end
