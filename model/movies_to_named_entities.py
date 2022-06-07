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


# https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy
# movies_to_named_entities_association_table = Table('movies_to_named_entities', Base.metadata,
#       Column('movie_id', ForeignKey('movies.movie_id'),primary_key=True),
#       Column('named_entity_value',primary_key=True),
#       Column('named_entity_tag',primary_key=True),
#       ForeignKeyConstraint(['named_entity_value', 'named_entity_tag'], ['named_entity.value', 'named_entity.tag'])
# )
# # __table_args__ = (ForeignKeyConstraint(['named_entity_value', 'named_entity_tag'], ['named_entity.value', 'named_entity.tag']),)
# #
class MoviesToNamedEntities(Base):
    __tablename__ = 'movies_to_named_entities'
    movie_id = Column(Integer, ForeignKey('movies.tmdb_id'), primary_key=True)
    named_entity_value = Column(String, primary_key=True)
    named_entity_tag = Column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['named_entity_value', 'named_entity_tag'],
            ['named_entities.value', 'named_entities.tag'],
        ),
    )
