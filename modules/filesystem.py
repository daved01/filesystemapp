import datetime

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
    

    def dfs(self, node: object, level=-1) -> None:
        if not node:
            return
        if level >= 0:
            print("   " * level, "|-", node._name)
        if type(node) == Folder and node._children:
            for child in node._children.keys():
                self.dfs(node._children[child], level+1)

     
    def add(self, paths: list[str]) -> None:
        """
        Takes list of paths and adds them to the tree.
        """
        for path in paths:
            raws = path.split("/")
            curr_node = self._root

            timestamp = datetime.datetime.now()
            for raw in raws:
                # File
                if len(raw.split(".")) == 2:
                    if raw in curr_node._children:
                        print(f"File {raw} already exists!")
                    else:
                        new_node = File("text", 16, timestamp)
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