"""
This module provides model classes for the Item Catalog App project.
"""

#pylint: disable=relative-import,no-init,too-few-public-methods,invalid-name,unused-argument

import re

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from catalog.database import Base

class User(Base):
    """A class to store information for a user."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Method to return serialized JSON object of class data."""

        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }

class Category(Base):
    """A class to store information for a category."""

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    url_name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Method to return serialized JSON object of class data."""

        return {
            'id': str(self.id),
            'name': self.name,
            'url_name': self.url_name,
            'user_id': str(self.user_id)
        }

class CategoryItem(Base):
    """A class to store information for a category item."""

    __tablename__ = 'category_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    url_name = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Method to return serialized JSON object of class data."""

        return {
            'id': str(self.id),
            'name': self.name,
            'url_name': self.url_name,
            'description': self.description,
            'category_id': str(self.category_id),
            'user_id': str(self.user_id)
        }


#
# Add events to listen for 'before_insert' to auto-set 'url_name' values.
#
# Sources:
#   - http://stackoverflow.com/questions/25161938/column-default-value-based-on-another-property
#   - http://docs.sqlalchemy.org/en/latest/core/event.html
#
@listens_for(Category, 'before_insert')
def category_defaults(mapper, configuration, target):
    """
    Function to set url_name attribute for Category object.
    """
    if not target.url_name:
        target.url_name = str_make_url_friendly(target)

@listens_for(CategoryItem, 'before_insert')
def category_item_defaults(mapper, configuration, target):
    """
    Function to set url_name attribute for CategoryItem object.
    """
    if not target.url_name:
        target.url_name = str_make_url_friendly(target)


def str_make_url_friendly(target):
    """
    Function to return lowercase value of specified string, with spaces
    as hyphens and all non-alphanumeric characters stripped out.
    """

    return re.sub(r'[^0-9a-zA-Z\-\_]', '', target.name.lower().replace(' ', '-'))
