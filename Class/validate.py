import re
from constants import MAC_PATTERN_MAP
from . import Decorator

class Validate :

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Mac (Mac) -> bool :
        for Pattern in MAC_PATTERN_MAP.values() :
            if re.match(Pattern , Mac) : return True
        return False