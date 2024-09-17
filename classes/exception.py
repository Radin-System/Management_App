class ContainerError:
    class NotFound(Exception):
        ...

    class Exists(Exception):
        ...

class AuthenticationError(Exception):
    ...

class RaiseFromList(Exception):
    '''Exception raised for specific error conditions.'''
    def __init__(self, error_list:list):
        self.error_list = error_list
        Message = ''
        for error in self.error_list:
            Message += f'{error.__class__.__name__}: {str(error)} , '
        super().__init__(Message[:-2])

__all__ = [
    'AuthenticationError',
    'RaiseFromList',
    'ServiceNotFoundError',
]