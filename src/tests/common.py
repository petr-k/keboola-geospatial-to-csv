import os


def data_file(relative_path):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/in/files",
        relative_path
    )
