# Lifelog Caption

Automatically caption lifelog images using a RNN.

## Setup

This is a doozy of a set up. This repository contains a script that will
(read: should) perform the steps required [here](https://github.com/karpathy/neuraltalk2#user-content-requirements).
Note that this will only work on **OSX**, I don't have (or need) setup
scripts for Windows or Linux, but if somehow you find this useful do not
be afraid to send a PR.

You will probably need to edit the `install.sh` shell script before you
even run it. I'm referring to the commands at the top of the file. Both
lines are documented on what you should do if your configuration differs
from mine (which is most likely will).

### Requirements:

Before you run the script, and after you have edited it, Please ensure 
you have the following tools/libraries installed:

 - gcc & g++ `Apple LLVM version 7.3.0 (clang-703.0.31)`
 - python `Python 3.5.1` (but 2.7.x *should* work)
 - brew `Homebrew 0.9.9` (yeah, you actually need this)
 
### Installing

Finally, once you have prepared your system for installation, and have 
configured the installation script, you can run it. Running the script
can be done by invoking `./install.sh` on your command line. This will
install a **LOT** of things and will take quite a while, including:

 - All the libraries and tools needed to run neuraltalk2
 - neuraltalk2 itself
 - The models required for neuraltalk2 to run
 
## Running

So far I have only included one script, which will go through and 
preprocess the annotations for use in training and evaluation. You can
invoke this script by running:

`./preprocess.sh /path/to/dataset.xml /path/to/images/ some_output.json 50`

Where `dataset.xml` is the data set distributed in the NTCIR-12
lifelogging task, and where `50` is the number of images to assign to 
validation data (for CV etc).

After this, you will have the `.json` and `.t7` files, and the training 
and evaluation can be done manually by following the instructions in the
neuraltalk2 repository.