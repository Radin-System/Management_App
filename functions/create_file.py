import os,shutil

def Create_VNC_File(Name:str,*,
        Folder:str,
        Host:str,
        Domain:str,
        ) -> str:
    
    Filename = f'{Host}.{Domain}.vnc'
    File = os.path.join(Folder,Filename)

    with open(File,'w') as f:
        f.write('ConnMethod=udp\n')
        f.write(f'FriendlyName={Name}@{Domain}\n')
        f.write(f'Host={Host}.{Domain}\n')
        f.write(f'Labels={Domain}\n')

    return Filename