#####################################################
# Run the whole [preprocess -> train -> eval] process
#####################################################

# First need to preprocess the data:
# Arguments: $1=/path/to/dataset.xml $2=/path/to/images $3=number of images to assign to validation data
echo Preprocessing...
./preprocess.sh $1 $2 output.json $3

# Next need to train
echo Training...
d=$(pwd)
cd $LIFELOG_CLASSIFICATION_DIR
# This assumes that the neuraltalk2 dir is inside the caption dir
th train.lua -input_h5 ../data.h5 -input_json ../data.json -gpuid -1 max_iters 100

# Whoop, now we can evaluate!
echo Evaluating...
th eval.lua -model model_id.json -image_folder $2 -num_images $3 -gpuid -1

echo Done!
echo You can see the results by running:
echo cd $LIFELOG_CLASSIFICATION_DIR/vis \&\& python -m SimpleHTTPServer

