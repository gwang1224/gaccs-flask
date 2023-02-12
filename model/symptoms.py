from sqlalchemy import Column, Integer, String
from .. import db


class Symptom(db.Model):
    # defining table
    __tablename__ = "symptom"
    id = Column(Integer, primary_key=True)
    _comment = Column(String(255), nullable=False)
    _symptom = Column(Integer, nullable=False)

    # initialization
    def __init__(self, comment, symptom):
        self._comment = comment
        self._symptom = symptom

    @property
    def comment(self):
        return self._comment

    @period.setter
    def text(self, comment):
        self._text = comment

    @property
    def symptom(self):
        return self._symptom

    @period.setter
    def text(self, symptom):
        self._text = symptom

    def to_dict(self):
        return {"id": self.id, "comment": self.comment, "symptom": self.symptom}

def init_schedules():
    task1 = Symptom(comment="Melatonin", symptom=1)
    task2 = Symptom(comment="Accutane", symptom=2)
    db.session.add(task1)
    db.session.add(task2)

    db.session.commit()