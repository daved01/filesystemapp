import argparse
import logging
import pickle
import os.path
import sys

import modules.filesystem as fs


if __name__== "__main__":  
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARN)
    logging.info(f"Python version: {sys.version}")
    # Load data if exists.
    filename = './data/data.pkl'  
    if os.path.exists(filename):
        filehandler = open(filename, 'rb')
        filesystem = pickle.load(filehandler)
        logging.info("Loaded existing folders.")
    else:
        filesystem = fs.FileSystem()
        logging.info("No existing folders found. Initilized folders.")

    # Parse arguments.
    parser = argparse.ArgumentParser(description="File application app.")
    parser.add_argument("command", choices = ["add", "view", "filter", "delete"], type=str, help="Command for app.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--path", default=None, help="Provide full path")
    group.add_argument("-f", "--filter", choices=["type", "name"], default=None)

    args = parser.parse_args()
    logging.info(f"User input: {args.command}")

    if args.command == "view":     
        filesystem.view()

    elif args.command == "add" and args.path:
        file_paths = filesystem.get_file_paths(args.path)
        filesystem.add(file_paths)
    
    elif args.command == "filter":
        print("Filter")
        if args.name:
            print("Name")
        elif args.type:
            print("Type")

    elif args.command == "delete" and args.path:
        filesystem.delete(args.path)
    
    logging.debug(f"Ran command {args.command}")
    # Save changes
    filehandler = open(filename, 'wb')
    pickle.dump(filesystem, filehandler)