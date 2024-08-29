from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class OwnerMixin:
    __abstract__ = True

    @declared_attr
    def owner(cls): 
        return relationship("User", backref=f"owned_{cls.__tablename__}")

    @declared_attr
    def owner_id(cls): 
        return Column(Integer, ForeignKey('users.id'), nullable=False)
