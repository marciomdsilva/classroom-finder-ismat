from flask import request, url_for
from requests import Response
from sqlalchemy import or_
from sqlalchemy.orm import relationship
from typing import List

from db import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


userCursos = db.Table('userCursos', db.Model.metadata,
    db.Column('id', db.Integer, db.ForeignKey('users.id')),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.curso_id'))
)

userCadeiras = db.Table('userCadeiras', db.Model.metadata,
    db.Column('id', db.Integer, db.ForeignKey('users.id')),
    db.Column('cadeira_id', db.Integer, db.ForeignKey('cadeiras.cadeira_id'))
)

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=0)  # 0=>aluno, 1=>professor, 2=>administracao

    cursos = relationship("CursoModel",
                    secondary=userCursos)
    cadeiras = relationship("CadeiraModel",
                    secondary=userCadeiras)
    confirmation = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def most_recent_confirmation(self) -> ConfirmationModel:
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, search: str = None) -> List["UserModel"]:
        if search is None:
            return cls.query.all()
        else:
            return cls.query.filter(or_(UserModel.name.contains(search), UserModel.email.contains(search), UserModel.username.contains(search)))

    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000 - /  +   /user_confirm/<id>
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
        subject = "Registration confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
