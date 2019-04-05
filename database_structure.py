
from sqlalchemy import Column, ForeignKey, Integer, String, Float, BIGINT, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import setting


Base = declarative_base()




class IMDB_Movie_Info(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(32), nullable=False)
    gender = Column(Integer, nullable=True)
    age = Column(Integer)
    major = Column(String(50))
    prefer = Column(String(50))
    telephone = Column(String(20))
    country = Column(String(50))
    state = Column(String(50))
    city = Column(String(50))
    session = Column(String(20))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'age': self.age,
            'major': self.major,
            'prefer': self.prefer,
            'weight': self.weight,
            'target_weight': self.target_weight,
            'telephone': self.telephone,
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'session': self.session
        }


engine = create_engine(setting.DB_URI)
Base.metadata.create_all(engine)

