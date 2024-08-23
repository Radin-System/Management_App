import os
from typing import Any
import os, uuid, json

ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Create(File_Name:str, Path:str, Data:Any, Mode:str='w') -> str:
    # Create File Path
    File_Path = os.path.join(Path, File_Name)
    # Ensure the directory exists
    os.makedirs(Path, exist_ok=True)

    with open(File_Path, Mode) as f:
        f.write(str(Data))
    
    return File_Path


def Vnc(Name:str,*,
        Folder:str,
        Host:str,
        Domain:str,
        ConnMethod:str='udp'
        ) -> str:
    
    File_Name = f'{Host}.{Domain}.vnc'
    Data = f'ConnMethod={ConnMethod}\nFriendlyName={Name}@{Domain}\nHost={Host}.{Domain}\nLabels={Domain}\n'
    
    return Create(File_Name,Folder,Data)

def ErrorFile(Data:dict) -> str:
    
    # Ensure the directory exists
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    # Generate a unique filename
    Unique_UID = uuid.uuid4()
    File_Name = f'{Unique_UID}.{ERROR_LOG_EXTENSION}'

    Create(File_Name,ERROR_LOG_DIR,Data=json.dumps(Data))

    return str(Unique_UID)
