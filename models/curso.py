from typing import List
from db import db


class CursoModel(db.Model):
    __tablename__ = "cursos"

    curso_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    cadeira = db.relationship("CadeiraModel", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name: str) -> "CursoModel":
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items Where name=name LIMIT 1

    @classmethod
    def find_by_id(cls, curso_id: int) -> "CursoModel":
        return cls.query.filter_by(curso_id=curso_id).first()  # SELECT * FROM items Where name=name LIMIT 1

    @classmethod
    def find_all(cls, search: str = None) -> List["CursoModel"]:
        if search is None:
            return cls.query.all()
        else:
            return cls.query.filter(CursoModel.name.contains(search))

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()