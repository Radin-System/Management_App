from sqlalchemy import Column, String

from classes.policy.input import *

class NameMixin:
    __abstract__  = True
    firstname_en  = Column(String(255), nullable=False, info={'Policy':NamePolicy_En})
    lastname_en   = Column(String(255), nullable=True, info={'Policy':NamePolicy_En})
    firstname_fa  = Column(String(255), nullable=False, info={'Policy':NamePolicy_Fa})
    lastname_fa   = Column(String(255), nullable=True, info={'Policy':NamePolicy_Fa})

    def calc_fullname(self) -> None:
        self.fullname_en = f'{self.firstname_en} {self.lastname_en if self.lastname_en is not None else ''}'.strip()
        self.fullname_fa = f'{self.firstname_fa} {self.lastname_fa if self.lastname_fa is not None else ''}'.strip()
