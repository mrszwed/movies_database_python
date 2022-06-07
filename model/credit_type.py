import sqlalchemy
from sqlalchemy import Column, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from model.base import Base


class CreditType(Base):
    __tablename__ = "credit_types"
    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"
