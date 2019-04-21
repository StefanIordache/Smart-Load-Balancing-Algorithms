import os


def create_directory(path):

    try:
        os.mkdir(path)
    except FileExistsError:
        print("File/Folder Exists - " + path)

    return path


def create_file(path, extension=""):
    f = open(path + extension, "w+")
    f.close()

    return path


def append_to_file(path, info):
    try:
        with open(path, "a") as file:
            file.write(info)
    except Exception as e:
        print("Append Error:\n" + str(e))
    return path


def write_to_file(path, info):
    try:
        with open(path, "w+") as file:
            file.write(info)
    except Exception as e:
        print("Append Error:\n" + str(e))
    return path
