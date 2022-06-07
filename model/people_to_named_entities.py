import json
import requests
import sqlalchemy
from sqlalchemy import Column, Table, ForeignKeyConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import configuration

from model.base import Base


#  movies_to_named_entities_association_table = Table('people_to_named_entities', Base.metadata,
#       Column('people_id', ForeignKey('person.people_id'),primary_key=True),
#       Column('named_entity_value',primary_key=True),
#       Column('named_entity_tag',primary_key=True),
#       ForeignKeyConstraint(['named_entity_value', 'named_entity_tag'], ['named_entity.value', 'named_entity.tag'])
# )

class PeopleToNamedEntities(Base):
    __tablename__ = 'people_to_named_entities'
    people_id = Column(Integer, ForeignKey('people.tmdb_id'), primary_key=True)
    named_entity_value = Column(String, primary_key=True)
    named_entity_tag = Column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['named_entity_value', 'named_entity_tag'],
            ['named_entities.value', 'named_entities.tag'],
        ),
    )
