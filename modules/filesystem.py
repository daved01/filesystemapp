import datetime
import os

import modules.tree


class File(modules.tree.TreeNode):
    def __init__(self, type: str, size: int, timestamp: object) -> None: 
        modules.tree.TreeNode.__init__(self, timestamp)
        self._type = type
        self._size = size


class Folder(modules.tree.TreeNode):
    def __init__(self, timestamp=None) -> None:
        modules.tree.TreeNode.__init__(self, timestamp)
        self._children = dict() # self._name -> object


class FileSystem:
    def __init__(self)-> None:
        self._root = Folder() # Emtpy top level root folder
        self._filetypes = {"txt": "text", "pdf": "text", "csv": "text",
                            "png": "image", "jpg": "image", "jpeg": "image"}
    

    def dfs(self, node: object, level=-1) -> None:
        if not node:
            return
        if level >= 0:     
            if type(node) == File:
                print("   " * level, "|-", node._name, " (",node._timestamp.strftime('%Y/%d/%m-%H:%m:%S'), ", ", node._type, ",", node._size, "kB )")
            else:
                print("   " * level, "|-", node._name)
        if type(node) == Folder and node._children:
            for child in node._children.keys():
                self.dfs(node._children[child], level+1)
    

    def get_file_paths(self, path_in: str) -> list[(str, float)]:
        """
        Returns list of full paths to all files at given path.
        Does not return path for empty folder.
        """
        paths_out = []
        for (path, dirs, files) in os.walk(path_in):
            for file in files:
                if file[0] != ".":
                    curr_path = path + "/" +file
                    curr_size = os.path.getsize(curr_path)
                    paths_out.append((curr_path, float(curr_size/1000))) # File size in kBs
        return paths_out
     

    def add(self, paths: list[(str, float)]) -> None:
        """
        Takes list of paths and adds them to the tree.
        """
        for raw_path in paths:
            path, size = raw_path[0], raw_path[1]

            # Remove leading slash symbol.
            if path[0] == "/":
                path = "".join(path[1:])
            raws = path.split("/")
            curr_node = self._root

            timestamp = datetime.datetime.now()
            for raw in raws:
                # File
                if len(raw.split(".")) == 2:
                    if raw in curr_node._children:
                        print(f"File {raw} already exists!")
                    else:
                        ext = raw.split(".")[1]
                        if ext in self._filetypes:
                            filetype = self._filetypes[ext]
                        else:
                            filetype = "other"
                        new_node = File(filetype, size, timestamp)
                        new_node._name = raw
                        curr_node._children[raw] = new_node
                # Folder
                else:
                    if raw in curr_node._children:
                        curr_node = curr_node._children[raw]
                    else:
                        new_node = Folder(timestamp)
                        new_node._name = raw
                        curr_node._children[raw] = new_node
                        curr_node = new_node
                    

    def filter(self, name=None) -> list[str]:
        # Top level view with details if no arg given
        raise NotImplementedError


    def delete(self, path: str) -> None:
        """
        Deletes file or folder at path.
        """
        path_list = path.split("/")
        curr_node = self._root

        for i in range(len(path_list)-1):
            path = path_list[i]
            curr_node = curr_node._children[path]
        del curr_node._children[path_list[-1]]
           

    

    def view(self) -> None:
        # Full tree view
        self.dfs(self._root)       