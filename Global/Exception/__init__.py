"""
class Template(CustomError):
    '''Exception raised for specific error conditions.'''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
"""
class CustomError(Exception):
    """Base class for custom exceptions."""
    pass

class RaiseFromList(CustomError):
    '''Exception raised for specific error conditions.'''
    def __init__(self, error_list):
        self.error_list = error_list
        Message = ''
        for error in self.error_list:
            Message += f'{error.__class__.__name__}: {str(error)} , '
        super().__init__(Message[:-2])