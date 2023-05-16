from flask import Flask

from datetime import datetime
from app.extensions import db


class FileSystem(db.Model):
    __tablename__ = "file_system"
    fid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)


class FileMetaData(db.Model):
    __tablename__ = "file_metadata"
    fid = db.Column(db.Integer, db.ForeignKey(FileSystem.fid), primary_key=True)
    name = db.Column(db.String, nullable=False)
    data = db.Column(db.String, server_default="", nullable=False)
    size = db.Column(db.Integer, server_default="0", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), server_default=datetime.now().isoformat(), nullable=False)


class Folders(db.Model):
    __tablename__ = "folders"
    fid = db.Column(db.Integer, db.ForeignKey(FileSystem.fid), primary_key=True)


def create_file(name: str, pid: int, data: str = ""):
    num_files = FileSystem.query.count()

    # Create instances
    fs_row = FileSystem(fid=num_files, pid=pid)
    mtd_row = FileMetaData(fid=num_files, name=name, data=data)

    # Establish parent-child relationship
    mtd_row.parent = fs_row

    # Add rows to database session
    db.session.add(fs_row)
    db.session.add(mtd_row)

    # Add to Folders table if `data` field is empty string
    if data == "":
        fld_row = Folders(fid=num_files)
        fld_row.parent = fs_row
        db.session.add(fld_row)

    # Commit changes to database
    db.session.commit()


def init(app: Flask):
    with app.app_context():
        db.create_all()
        create_file(name="/", pid=0, data="")
