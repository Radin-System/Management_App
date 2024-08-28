from typing import Any
from classes.validator import *
from functions.convert import CleanStr, LowerCase, StrToSha

class ColoumnInfo:
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
        if not isinstance(Other, ColoumnInfo):
            raise NotImplementedError('You can only add ColoumnInfo with each other')

        # Combine lists
        Combined_Validators = self.Validators + (Other.Validators or [])
        Combined_Convertors = self.Convertors + (Other.Convertors or [])

        # Combine booleans with the custom logic
        Combined_Changeable = self._combine_bools(self.Changeable, Other.Changeable)
        Combined_Visible = self._combine_bools(self.Visible, Other.Visible)
        Combined_First_Convert = self._combine_bools(self.First_Convert, Other.First_Convert)

        return ColoumnInfo(
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
BasePolicy     = ColoumnInfo()

# Level One
FirstConvert   = BasePolicy + ColoumnInfo(First_Convert=True)
CleanString    = BasePolicy + ColoumnInfo(Convertors=[CleanStr])
NotChangeble   = BasePolicy + ColoumnInfo(Changeable=False)
EnsureInteger  = BasePolicy + ColoumnInfo(Convertors=[int])
HiddenField    = BasePolicy + ColoumnInfo(Visible=False)
PasswordPolicy = BasePolicy + ColoumnInfo(Validators=[Password], Convertors=[StrToSha])

# Level Two
NamePolicy_En  = CleanString + ColoumnInfo(Validators=[English])
NamePolicy_Fa  = CleanString + ColoumnInfo(Validators=[Persian])
MobilePolicy   = CleanString + ColoumnInfo(Validators=[MobileNumber])

# Level Three
UsernamePolicy = CleanString + NotChangeble + FirstConvert + ColoumnInfo(Validators=[EnglishSpecial, Username], Convertors=[LowerCase])
EmailPolicy    = CleanString + NotChangeble + FirstConvert + ColoumnInfo(Validators=[EnglishSpecial, Email], Convertors=[LowerCase])
BaseInfoPolicy = HiddenField + NotChangeble
UuidPolicy     = HiddenField + NotChangeble + ColoumnInfo(Validators=[Uuid])

__all__ = [
    'ColoumnInfo',
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
## Results
"""
BasePolicy : {'Setattr': {'Validators': [], 'Convertors': []}, 'Flags': {'Visible': None, 'Changeable': None}}
CleanString : {'Setattr': {'Validators': [], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': None}}
NotChangeble : {'Setattr': {'Validators': [], 'Convertors': []}, 'Flags': {'Visible': None, 'Changeable': False}}
EnsureInteger : {'Setattr': {'Validators': [], 'Convertors': [<class 'int'>]}, 'Flags': {'Visible': None, 'Changeable': None}}
HiddenField : {'Setattr': {'Validators': [], 'Convertors': []}, 'Flags': {'Visible': False, 'Changeable': None}}
NamePolicy_En : {'Setattr': {'Validators': [<class 'classes.validator.english.English'>], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': None}}
NamePolicy_Fa : {'Setattr': {'Validators': [<class 'classes.validator.persian.Persian'>], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': None}}
PasswordPolicy : {'Setattr': {'Validators': [<class 'classes.validator.password.Password'>], 'Convertors': [<function StrToSha at 0x0000016D42E7D580>]}, 'Flags': {'Visible': None, 'Changeable': None}}
UsernamePolicy : {'Setattr': {'Validators': [<class 'classes.validator.english_special.EnglishSpecial'>, <class 'classes.validator.username.Username'>], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': None}}
MobilePolicy : {'Setattr': {'Validators': [<class 'classes.validator.mobile_number.MobileNumber'>], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': None}}
EmailPolicy : {'Setattr': {'Validators': [<class 'classes.validator.english_special.EnglishSpecial'>, <class 'classes.validator.email.Email'>], 'Convertors': [<function CleanStr at 0x0000016D42616660>]}, 'Flags': {'Visible': None, 'Changeable': False}}
BaseInfoPolicy : {'Setattr': {'Validators': [], 'Convertors': []}, 'Flags': {'Visible': False, 'Changeable': False}}
"""