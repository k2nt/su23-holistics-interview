import os
from typing import List

from app.extensions import db
from app.models.fs import FileSystem
from app.models.fs import MetaData
from app.models.fs import Content

from app.lib import service_logging as sv_logging


def get_file_count() -> int:
    """Get total number of files in file system

    Return:
        int
    """
    return FileSystem.query.count()


def create_file(
        path: str,
        pid: int,
        data: str = "",
        is_folder: bool = False
) -> int:
    """Create file or folder

    Args:
        path: str -- File name with respect to root folder
        pid: int -- ID of parent folder
        data: str = "" -- File content
        is_folder: bool = False -- Whether this is a folder

    Return:
        int -- The file ID

    Raise:
        Exception -- If file/folder was not created
    """
    print("Create File", data, is_folder)

    # A file cannot already exist at given path
    try:
        get_file_id(path, is_folder=is_folder)
        raise FileExistsError(f"{'folder' if is_folder else 'file'} already exist")
    except FileNotFoundError:
        pass

    # File ID is the current number of files in file system
    fid = get_file_count()

    # Create FileSystem row
    fs_row = FileSystem(fid=fid, pid=pid)
    db.session.add(fs_row)

    # Create MetaData row
    mtd_row = MetaData(fid=fid, path=path, size=len(data), is_folder=is_folder)
    mtd_row.parent = fs_row
    db.session.add(mtd_row)

    # Create Content row
    # This only happens if a file is being created
    if not is_folder:
        print("Content", data)
        ctn_row = Content(fid=fid, data=data)
        ctn_row.parent = fs_row
        db.session.add(ctn_row)

        # Add file size to parent folder size
        size = len(data)
        full_path = path.split("/")
        for i in range(1, len(full_path)+1):
            folder_path = "/".join(full_path[:-i])
            row: MetaData = MetaData.query.filter(MetaData.path == folder_path).first()
            row.size += size

    # Commit transactions to database
    db.session.commit()

    return fid


def get_file_id(path: str, is_folder: bool = False) -> int:
    """Get file id from path name

    Args:
        path: str -- File name with respect to root folder
        is_folder: bool = False -- Whether to search for a folder

    Return:
        int -- File ID

    Raise:
        FileNotFoundError -- If file does not exist
    """
    row: MetaData = MetaData.query.filter(
        MetaData.path == path, MetaData.is_folder == is_folder
        ).first()
    if not row:
        raise FileNotFoundError(f"{'folder' if is_folder else 'file'} not found")

    return row.fid


def create_folder_path(folder_path: List[str]) -> int:
    """Creates folder structure

    Args:
        folder_path: List[str] -- Folder path with respect to root folder

    Return:
        int -- Folder ID

    Raise:
        FileExistsError -- If folder already exist
    """
    if not folder_path:
        return 0

    # A folder cannot already exist at given path
    try:
        get_file_id("/".join(folder_path), is_folder=True)
        raise FileExistsError("folder already exist")
    except FileNotFoundError:
        pass

    # Default to root folder
    path, pid = "", 0

    for folder in folder_path:
        path = os.path.join(path, folder)

        # Create intermediate folder if not exist
        try:
            get_file_id(path, is_folder=True)
        except FileNotFoundError:
            pid = create_file(path=path, pid=pid, is_folder=True)

    return pid


def list_subfiles(path: str) -> List[MetaData]:
    """List files and folders directly under given folder path

    Args:
        path: str -- Folder path

    Return:
        List[str] -- File and folder names

    Raise:
        FileNotFoundError -- If no folder is found at path
    """
    try:
        fid = get_file_id(path, is_folder=True)
        cfids = [row.fid for row in FileSystem.query.filter(FileSystem.pid == fid).all()]
        mtds = [mtd.as_dict() for mtd in MetaData.query.filter(MetaData.fid.in_(cfids)).all()]
        return mtds
    except FileNotFoundError:
        raise FileNotFoundError("folder not found")


def get_file_content(path: str) -> str:
    """Get file content

    Args:
        path: str -- File path

    Return:
        str

    Raise:
        FileNotFoundError -- If no file is found at path
    """
    try:
        fid = get_file_id(path)
        row: Content = Content.query.filter(Content.fid == fid).first()
        return row.data
    except FileNotFoundError:
        raise FileNotFoundError("file not found")
