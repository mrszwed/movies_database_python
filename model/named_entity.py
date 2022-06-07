from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from model.base import Base
from sqlalchemy import String

# from model.movies_to_named_entities import movies_to_named_entities_association_table, MoviesToNamedEntities
from model.movies_to_named_entities import MoviesToNamedEntities
from model.people_to_named_entities import PeopleToNamedEntities


class NamedEntity(Base):
    __tablename__ = "named_entities"
    value = Column(String, primary_key=True)
    tag = Column(String, primary_key=True)
    PrimaryKeyConstraint(value, tag, name='uniq_1')
    movies = relationship("Movie", secondary='movies_to_named_entities', back_populates="named_entities")
    people = relationship("Person", secondary='people_to_named_entities', back_populates="named_entities")
    reviews = relationship("Review", secondary='reviews_to_named_entities', back_populates="named_entities")

    def __init__(self, **kwargs):
        self.value = kwargs.get('value')
        self.tag = kwargs.get('tag')

    def __repr__(self):
        return f"{self.value} {self.tag}"
