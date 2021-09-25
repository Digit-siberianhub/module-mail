from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120))
    unread = Column(Integer)
    new = Column(Integer)

    def __repr__(self):
        return f'<User: {self.email}>'
