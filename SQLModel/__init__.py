from sqlalchemy                 import Column , Integer , String , DateTime , Text , text , Boolean
from sqlalchemy.orm             import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CustomColumn(Column):
    __visit_name__ = "column"
    inherit_cache = True

    def __init__(self , *args , **kwargs):

        super().__init__(*args, **kwargs)

class infoMixin(Base):
    __abstract__ = True

class ownerMixin(Base):
    __abstract__ = True

    owner_id = CustomColumn()
    owner = relationship()

Models = [
]
