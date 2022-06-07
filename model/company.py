import json
import requests
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from model.base import Base
from model.movies_to_companies import movies_to_companies_association_table


class Company(Base):
    __tablename__ = "companies"
    tmdb_id = Column(Integer, primary_key=True)
    description = Column(String)
    headquarters = Column(String)
    homepage = Column(String)
    logo_path = Column(String)
    name = Column(String)
    origin_country = Column(String)
    parent_company = Column(Integer, ForeignKey('companies.tmdb_id'))
    # parent = relationship("Company", back_populates="children", uselist=False)
    parent = relationship("Company", uselist=False)
    # children=relationship("Company", back_populates="parent", remote_side="companies.parent_company")
    movies = relationship("Movie", secondary=movies_to_companies_association_table, back_populates="companies")

    def __init__(self, **kwargs):  # slownik key word arguments
        self.tmdb_id = kwargs.get('id')
        self.description = kwargs.get('description')
        self.headquarters = kwargs.get('headquarters')
        self.homepage = kwargs.get('homepage')
        self.logo_path = kwargs.get('logo_path')
        self.name = kwargs.get('name')
        self.origin_country = kwargs.get('origin_country')
        parent_company = kwargs.get('parent_company')
        if parent_company is not None:
            self.parent = Company(**parent_company)

    def __repr__(self):
        return f"{self.name} {self.headquarters} {self.origin_country} {self.description}"

    @staticmethod
    def get_company(API_key, company_id):
        query = 'https://api.themoviedb.org/3/company/' + str(company_id) + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            text = json.dumps(array)
            return Company(**array)  # array - slownik, zwracany przez response
        else:
            return None
