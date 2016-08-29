# If you have a whole bunch of images and you want 
# to flatten them so that they all appear in the 
# same directory, this script is for you!

import sys, os, shutil

def main(args):
    if len(args) < 2:
        print("Usage: flatten.py /path/to/root/dir /path/to/new/dir/")
        sys.exit(2)

    if not os.path.exists(args[1]):
        os.makedirs(args[1])

    for root, dirs, files in os.walk(args[0]):
        for file in files:
            shutil.copy(root + "/" + file, args[1] + file)


if __name__ == "__main__":
    main(sys.argv[1:])
