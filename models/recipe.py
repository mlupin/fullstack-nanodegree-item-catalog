from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from models.base import Base
from models.category import Category
from models.user import User


class Recipe(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    insert_date = Column(DateTime(timezone=True), default=func.now())
    last_update = Column(DateTime(timezone=True), default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id'         : self.id,
            'insert_date': self.insert_date,
            'last_update': self.last_update
        }
