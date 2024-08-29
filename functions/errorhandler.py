import os, io, traceback
from datetime import datetime
from .create_file import ErrorFile

ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Handle_Error(Error:Exception,*, 
    Code:int = None, 
    Description:str = None, 
    **KWargs
    ) -> dict:

    # Ensure the directory exists
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    # Extracting the traceback and putting it in a var
    Traceback_Str = io.StringIO()
    if Error.__traceback__ is not None:
        traceback.print_exception(type(Error), Error, Error.__traceback__, file=Traceback_Str)
        Traceback_Content = Traceback_Str.getvalue()
    else:
        Traceback_Content = "No traceback available"

    # Constructing the error dictionary
    Dict = dict(
        name=type(Error).__name__,
        description=str(Error) if Description is None else Description,
        code=int(Code) if Code is not None else None,
        traceback=Traceback_Content,
        timestamp=str(datetime.now()),
        **KWargs
    )

    # Generate a unique identifier (UID) and store the error data
    UID = ErrorFile(Data=Dict)
    Dict['uid'] = UID

    return Dict