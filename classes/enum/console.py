from enum import Enum, auto

class RespondHeader(Enum):
    Info = '+ '
    Error = '- '
    Terminal = '>>'
    Input = '<<'
    Space = '  '
    Nothing = ''

class InputType(Enum):
    Raw = auto()
    Password = auto()