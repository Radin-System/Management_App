from classes.validator import *
from functions.convert import CleanStr, LowerCase, StrToSha

from ._base import InputPolicy

# Base Level
BasePolicy     = InputPolicy()

# Level One
FirstConvert   = BasePolicy + InputPolicy(First_Convert=True)
CleanString    = BasePolicy + InputPolicy(Convertors=[CleanStr])
NotChangeble   = BasePolicy + InputPolicy(Changeable=False)
EnsureInteger  = BasePolicy + InputPolicy(Convertors=[int])
HiddenField    = BasePolicy + InputPolicy(Visible=False)
PasswordPolicy = BasePolicy + InputPolicy(Validators=[Password], Convertors=[StrToSha])

# Level Two
NamePolicy_En  = CleanString + InputPolicy(Validators=[English])
NamePolicy_Fa  = CleanString + InputPolicy(Validators=[Persian])
MobilePolicy   = CleanString + InputPolicy(Validators=[MobileNumber])

# Level Three
UsernamePolicy = CleanString + NotChangeble + FirstConvert + InputPolicy(Validators=[EnglishSpecial, Username], Convertors=[LowerCase])
EmailPolicy    = CleanString + NotChangeble + FirstConvert + InputPolicy(Validators=[EnglishSpecial, Email], Convertors=[LowerCase])
BaseInfoPolicy = HiddenField + NotChangeble
UuidPolicy     = HiddenField + NotChangeble + InputPolicy(Validators=[Uuid])
