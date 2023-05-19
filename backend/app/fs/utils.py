import os


def normalize_path(path: str) -> str:
    # Normalize relative imports
    # e.g. a/b/../c -> a/c
    # e.g. a/b/./c -> a/b/c
    path = os.path.normpath(path)

    # Handle empty paths
    # Empty paths are multiple forward slashes clumped together
    # e.g. a///b -> a/b
    path = "/".join([tok for tok in path.split("/") if tok != ''])

    if path == ".":
        path = ""

    return path
