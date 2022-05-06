import modules.filesystem


def test_add_two_correct_paths():
    fs = modules.filesystem.FileSystem()

    paths = [("/base/folder1/file1.txt", 0.0), ("/base/folder2/file2.txt", 0.1)]
    fs.add(paths)

    # Check tree
    curr = fs._root
    assert isinstance(curr._children["base"], modules.filesystem.Folder), "Should be type folder."

    curr = curr._children["base"]
    assert len(curr._children) == 2, "Should be two folders."
    folder1 = curr._children["folder1"]
    folder2 = curr._children["folder2"]

    file1 = folder1._children["file1.txt"]
    file2 = folder2._children["file2.txt"]

    # Check files
    assert isinstance(file1, modules.filesystem.File), "Should be file."
    assert isinstance(file2, modules.filesystem.File), "Should be file."
    assert file1._size == 0.0, "Should be float(0.0)."
    assert file2._size == 0.1, "Should be float(0.1)."


def test_add_one_incorrect_paths():
    fs = modules.filesystem.FileSystem()
    # Paths should have leading slashes but don't have to.
    paths = [("base/folder1/file1.txt", 0.3)]
    fs.add(paths)
     # Check tree
    curr = fs._root
    assert isinstance(curr._children["base"], modules.filesystem.Folder), "Should be type folder."


def test_path_should_be_tuple():
    fs = modules.filesystem.FileSystem()
    paths = ["/base/folder1/file1.txt"]
    fs.add(paths)
    # Check tree
    curr = fs._root
    assert curr._name == None, "Should be empty."
    