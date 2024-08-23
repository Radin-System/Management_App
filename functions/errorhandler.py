import os, io, traceback
from datetime import datetime
from .create_file import ErrorFile

ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Handle_Error(Error:Exception,*,
        Code:int=None, 
        Description:str=None,
        **KWargs
        ) -> str:

    # Ensure the directory exists
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    # Extracting the traceback and putting it in a var
    Traceback_Str = io.StringIO()
    traceback.print_exception(type(Error), Error, Error.__traceback__, file=Traceback_Str)
    Traceback_Content = Traceback_Str.getvalue()

    Dict = dict(
        name = type(Error).__name__,
        description = str(Error) if Description is None else Description,
        code = int(Code),
        traceback = str(Traceback_Content),
        timestamp = str(datetime.now()),
        **KWargs
        )

    UID = ErrorFile(Data=Dict)
    Dict['uid'] = UID

    return Dict
