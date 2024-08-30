from classes.validator import *
from classes.convert import StringTool

from ._base import InputPolicy

# Base Level
BasePolicy     = InputPolicy('BasePolicy')

# Level One
FirstConvert   = BasePolicy + InputPolicy('FirstConvert', First_Convert=True)
CleanString    = BasePolicy + InputPolicy('CleanString', Convertors=[StringTool.Strip])
NotChangeble   = BasePolicy + InputPolicy('NotChangeble', Changeable=False)
EnsureInteger  = BasePolicy + InputPolicy('EnsureInteger',  Convertors=[int])
HiddenField    = BasePolicy + InputPolicy('HiddenField', Visible=False)
PasswordPolicy = BasePolicy + InputPolicy('PasswordPolicy', Validators=[Password], Convertors=[StringTool.Sha256])

# Level Two
NamePolicy_En  = CleanString + InputPolicy('NamePolicy_En', Validators=[English])
NamePolicy_Fa  = CleanString + InputPolicy('NamePolicy_Fa',Validators=[Persian])
MobilePolicy   = CleanString + InputPolicy('MobilePolicy',Validators=[MobileNumber])

# Level Three
UsernamePolicy = CleanString + NotChangeble + FirstConvert + InputPolicy('UsernamePolicy', Validators=[EnglishSpecial, Username], Convertors=[StringTool.Lower])
EmailPolicy    = CleanString + NotChangeble + FirstConvert + InputPolicy('EmailPolicy', Validators=[EnglishSpecial, Email], Convertors=[StringTool.Lower])
BaseInfoPolicy = HiddenField + NotChangeble + InputPolicy('BaseInfoPolicy')
UuidPolicy     = HiddenField + NotChangeble + InputPolicy('UuidPolicy', Validators=[Uuid])
