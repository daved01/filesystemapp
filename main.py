import argparse
import logging
import pickle
import os.path

import modules.filesystem as fs



if __name__== "__main__":  
    parser = argparse.ArgumentParser(description="File application app")
    parser.add_argument('--add', default=None, help="Select path to add")
    parser.add_argument('--delete', default=None, help="Select path to delete. Deletes all subfolders and files.")
    parser.add_argument('--view', default=None, help="Shows all subfolders and files.")
    # TODO: How to do filter with multiple options?

    args = parser.parse_args()


    # Load data if exists.
    filename = './data/data.pkl'  
    if os.path.exists(filename):
        filehandler = open(filename, 'rb')
        filesystem = pickle.load(filehandler)
    else:
        filesystem = fs.FileSystem()


    # Get this list from some other function that traverses paths.
    new_files = ["base/file1.txt", "base/folder2/file2.txt", "base2/file14.txt"]
    filesystem.add(new_files)

    filesystem.view()


    filesystem.delete("base")


    filesystem.view()

    # Save changes
    filehandler = open(filename, 'wb')
    pickle.dump(filesystem, filehandler)