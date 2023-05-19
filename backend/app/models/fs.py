from sqlalchemy import CheckConstraint

from datetime import datetime
from app.extensions import db


class FileSystem(db.Model):
    __tablename__ = "file_system"
    fid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MetaData(db.Model):
    __tablename__ = "metadata"
    fid = db.Column(db.Integer, db.ForeignKey(FileSystem.fid), primary_key=True)
    path = db.Column(db.String, nullable=False, index=True)
    is_folder = db.Column(db.Boolean, default=False, server_default="false", nullable=False)
    size = db.Column(db.Integer, default=0, server_default="0", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), server_default=datetime.now().isoformat(), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Content(db.Model):
    __tablename__ = "content"
    fid = db.Column(db.Integer, db.ForeignKey(FileSystem.fid), primary_key=True)
    data = db.Column(db.String, default="", server_default="")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
