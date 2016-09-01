#####################################################
# Run the whole [preprocess -> train -> eval] process
#####################################################

# First need to preprocess the data:
# Arguments: $1=/path/to/dataset.xml $2=num validation $3=num test
echo Preprocessing...
./preprocess.sh $1 output.json $2 $3

# Next need to train
echo Training...
d=$(pwd)
cd $LIFELOG_CLASSIFICATION_DIR
# This assumes that the neuraltalk2 dir is inside the caption dir
th train.lua -input_h5 ../data.h5 -input_json ../data.json -gpuid -1 -max_iters 10000

# Whoop, now we can evaluate!
echo Evaluating...
th eval.lua -model model_id.json -image_folder ../images -num_images -1 -gpuid -1 -dump_json 1

echo Done!
echo You can see the results by running:
echo cd $LIFELOG_CLASSIFICATION_DIR/vis \&\& python -m SimpleHTTPServer

