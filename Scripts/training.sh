#!/bin/bash  

# Start Training Session


TRAINING_TYPE=$1
DATA_SET_ID=$2
NUMBER_OF_EPOCHS=$3
OUTPUT_FILE_FORMAT=$4
OUTPUT_FREQUENCY=$5
COMMAND="python ../LoadBalancing/RL/training_launcher.py"

COMMAND="$COMMAND --training_type=$TRAINING_TYPE"
COMMAND="$COMMAND --data_set_id=$DATA_SET_ID"
COMMAND="$COMMAND --number_of_epochs=$NUMBER_OF_EPOCHS"
COMMAND="$COMMAND --out_file=$OUTPUT_FILE_FORMAT"
COMMAND="$COMMAND --out_freq=$OUTPUT_FREQUENCY"

echo $COMMAND

gnome-terminal --window-with-profile=WINDOW_KEEP_OPEN --command="$COMMAND"
