from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    submenu = relationship('Submenu', back_populates='menu', cascade='all, delete')


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), nullable=False)
    menu = relationship("Menu", back_populates='submenu')
    # -----------------------------------------------------------
    dish = relationship('Dish', back_populates='submenu', cascade='all, delete')

    def get_count_dish(self):
        return len(self.dish)

class Dish(Base):
    __tablename__ = 'dishs'
    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(String(20), nullable=False)

    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship("Submenu", back_populates='dish')



