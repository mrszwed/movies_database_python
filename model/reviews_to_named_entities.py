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


class ReviewsToNamedEntities(Base):
    __tablename__ = 'reviews_to_named_entities'
    review_id = Column(String, ForeignKey('reviews.id'), primary_key=True)
    named_entity_value = Column(String, primary_key=True)
    named_entity_tag = Column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['named_entity_value', 'named_entity_tag'],
            ['named_entities.value', 'named_entities.tag'],
        ),
    )
