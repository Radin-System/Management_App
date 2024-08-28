from typing import Any
from classes.validator import *
from functions.convert import CleanStr, LowerCase, StrToSha

class ColumnInfo:
    def __init__(self,*,
        Validators:list=None,
        Convertors:list=None,
        Changeable:bool=None,
        Visible:bool=None,
        First_Convert:bool=None,
        ) -> None:
        
        self.Validators = Validators or []
        self.Convertors = Convertors or []
        self.Changeable = Changeable
        self.Visible = Visible
        self.First_Convert = First_Convert

    def __add__(self, Other):
        if not isinstance(Other, ColumnInfo):
            raise NotImplementedError('You can only add ColumnInfo with each other')

        # Combine lists
        Combined_Validators = self.Validators + (Other.Validators or [])
        Combined_Convertors = self.Convertors + (Other.Convertors or [])

        # Combine booleans with the custom logic
        Combined_Changeable = self._combine_bools(self.Changeable, Other.Changeable)
        Combined_Visible = self._combine_bools(self.Visible, Other.Visible)
        Combined_First_Convert = self._combine_bools(self.First_Convert, Other.First_Convert)

        return ColumnInfo(
            Validators=Combined_Validators,
            Convertors=Combined_Convertors,
            Changeable=Combined_Changeable,
            Visible=Combined_Visible,
            First_Convert=Combined_First_Convert,
        )

    def Dict(self) -> dict:
        return {
            'Setattr': {
                'Validators':self.Validators,
                'Convertors':self.Convertors,
                },
            'Flags':{
                'Visible':self.Visible,
                'Changeable':self.Changeable,
                'First_Convert':self.First_Convert,
                },
        }

    @staticmethod
    def _combine_bools(First:bool|None, Second:bool|None) -> bool:
        if Second is None: 
            return First
        return Second

    def Apply(self, Input:Any) -> Any:

        if self.First_Convert:
            for Convertor in self.Convertors:
                Input = Convertor(Input)

            for Validator in self.Validators:
                Validator(Input)

        else:
            for Validator in self.Validators:
                Validator(Input)

            for Convertor in self.Convertors:
                Input = Convertor(Input)

        return Input

# Base Level
BasePolicy     = ColumnInfo()

# Level One
FirstConvert   = BasePolicy + ColumnInfo(First_Convert=True)
CleanString    = BasePolicy + ColumnInfo(Convertors=[CleanStr])
NotChangeble   = BasePolicy + ColumnInfo(Changeable=False)
EnsureInteger  = BasePolicy + ColumnInfo(Convertors=[int])
HiddenField    = BasePolicy + ColumnInfo(Visible=False)
PasswordPolicy = BasePolicy + ColumnInfo(Validators=[Password], Convertors=[StrToSha])

# Level Two
NamePolicy_En  = CleanString + ColumnInfo(Validators=[English])
NamePolicy_Fa  = CleanString + ColumnInfo(Validators=[Persian])
MobilePolicy   = CleanString + ColumnInfo(Validators=[MobileNumber])

# Level Three
UsernamePolicy = CleanString + NotChangeble + FirstConvert + ColumnInfo(Validators=[EnglishSpecial, Username], Convertors=[LowerCase])
EmailPolicy    = CleanString + NotChangeble + FirstConvert + ColumnInfo(Validators=[EnglishSpecial, Email], Convertors=[LowerCase])
BaseInfoPolicy = HiddenField + NotChangeble
UuidPolicy     = HiddenField + NotChangeble + ColumnInfo(Validators=[Uuid])

__all__ = [
    'ColumnInfo',
    'BasePolicy',
    'CleanString',
    'NotChangeble',
    'EnsureInteger',
    'HiddenField',
    'NamePolicy_En',
    'NamePolicy_Fa',
    'PasswordPolicy',
    'UsernamePolicy',
    'MobilePolicy',
    'EmailPolicy',
    'BaseInfoPolicy',
    'UuidPolicy',
]