from typing import List

from app.fs import repo as rp
from app.fs.utils import normalize_path


def create_file(path: str, force_create: bool = False, data: str = ""):
    """Create file or folder

    Args:
        path: str -- File path
        force_create: bool = False -- If `True`, create folder structure to that file
        data: str = "" -- File data, if empty string then it is a folder

    Raise:
        Exception -- If file/folder was not created
    """
    # Parse and normalize file path
    path = normalize_path(path)
    folder_path = path.split("/")[:-1]

    is_folder = (data == "")

    if force_create:
        # Create folder path if `force_create` is toggled `True`
        pid = rp.create_folder_path(folder_path)
    else:
        # Else, get file ID of parent folder
        pid = rp.get_file_id("/".join(folder_path), is_folder=True)

    rp.create_file(path=path, pid=pid, data=data, is_folder=is_folder)


def list_subfiles(path: str) -> List[str]:
    """List subfiles under a folder

    Args:
        path: str -- Folder path

    Return:
        List[str] -- List of files and folders directly under given folder path

    Raise:
        Exception
    """
    path = normalize_path(path)
    return rp.list_subfiles(path)


def get_file_content(path: str) -> str:
    """

    :param path:
    :return:
    """
    path = normalize_path(path)
    return rp.get_file_content(path)
