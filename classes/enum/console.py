import getpass
from enum import Enum

class RespondHeader(Enum):
    Info = '+ '
    Error = '- '
    Terminal = '>>'
    Input = '<<'
    Space = '  '
    Nothing = ''

class InputType(Enum):
    Raw = input
    Password = getpass