#############################################################################
# This setup script will install all the dependencies needed for neuraltalk2:
# https://github.com/karpathy/neuraltalk2
# PRs welcome :)
#############################################################################

echo Here we go, you may want to go grab a cup of coffee...

# You may need to change these depending on what you have.
# The rest of the steps require at least >= 4.6
# see https://e-lab.github.io/html/wiki-torch7-installation.html#torch-7-installation-on-mac-os-x
export CC=/usr/local/bin/gcc-6
export CXX=/usr/local/bin/g++-6

# I'm using zsh, so you'll need to change `zsh` to `bash` if you're not using zsh.
curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-all | zsh

# hopefully you've gotten this far ~
luarocks install nn
luarocks install nngraph
luarocks install image

# we have to install this one manually urgh ;)
wget http://www.kyne.com.au/~mark/software/download/lua-cjson-2.1.0.tar.gz
tar -xf lua-cjson-2.1.0.tar.gz
cd lua-cjson-2.1.0
luarocks make

# more dependencies we have to make ourselves
brew tap homebrew/science
brew install hdf5
git clone https://github.com/deepmind/torch-hdf5
cd torch-hdf5
luarocks make hdf5-0-0.rockspec
cd ../ && rm -rf torch-hdf5

# last one, I promise!
pip install h5py

echo Done!
echo Gonna go install the neuraltalk2 project for you now!

# Finally, exciting stuff
wget https://github.com/karpathy/neuraltalk2/archive/master.zip
unzip master
rm master.zip

# woo-hoo!
echo You are all set! You need to use an environment variable for everything else to work. Add the following to your .*shrc:
echo export LIFELOG_CLASSIFICATION_DIR=$(pwd)/neuraltalk2-master

