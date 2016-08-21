#############################################################################
# This setup script will preprocess the lifelog images for use in neuraltalk2
#############################################################################

python $1 $2 $3
python neuraltalk2-master/prepro.py --input_json $3 $4