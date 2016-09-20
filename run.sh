#####################################################
# Run the whole [preprocess -> train -> eval] process
#####################################################

# First need to preprocess the data:
# Arguments: $1=/path/to/dataset.xml $2=num validation $3=num test
#
# example:
# ./run.sh /Volumes/ext/data/ntcir2015_lifelogging/NTCIR_Lifelog_formal_run_Dataset/NTCIR-Lifelog_formal_run_dataset.xml 300 300
echo Preprocessing...
./preprocess.sh $1 output.json $2 $3

# Next need to train
echo Training...
d=$(pwd)
cd $LIFELOG_CLASSIFICATION_DIR
# This assumes that the neuraltalk2 dir is inside the caption dir
# TODO -> training didn't work for me, but I want to come back to it later
#th train.lua -input_h5 ../data.h5 -input_json ../data.json -gpuid -1 -max_iters 50000 -save_checkpoint_every 1000

# Whoop, now we can evaluate!
echo Evaluating...
# The crappy output is saved into a text file so we can process it into something better
th eval.lua -model model/model_id1-501-1448236541.t7_cpu.t7 -image_folder images -num_images -1 -gpuid -1 -dump_json 1 >> out.txt

python3 process-eval.py out.txt out.json
echo finished processing, the file is located at $(pwd)/out.json

echo Done!
echo You can see the results by running:
echo cd $LIFELOG_CLASSIFICATION_DIR/vis \&\& python -m SimpleHTTPServer