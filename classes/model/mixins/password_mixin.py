from sqlalchemy import Column, String, Boolean

from classes.policy.input import *

class PasswordMixin:
    __abstract__ = True
    password     = Column(String, nullable=False, info={'Policy':PasswordPolicy})
    expired_password = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})

    def reset_password(self,*,
            New:str,
            Confirm:str,
            Expire:bool=True
            ) -> None:

        if New == Confirm:
            self.password = New
            self.expired_password = bool(Expire)

        else:
            raise ValueError('Provided passwords do not match')

    def change_password(self,*,
        Old:str,
        New:str,
        Confirm:str,
        ) -> None:

        Old = PasswordPolicy.Apply(New)

        if New == Confirm:
            if self.password == Old:
                self.password = New

            else:
                raise ValueError('Provided passwords is incorrect')

        else:
            raise ValueError('Provided passwords do not match')
