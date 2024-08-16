import os,shutil

def Create_VNC_File(Name,*,Host,Domain) -> str:
    # Defining Local Vars
    Temp_Folder = '.temp/'
    Session_Folder = 'Z:\\IT\\Technical\\Group\\# VNC Sessions\\'
    Filename = f'{Host}.{Domain}.vnc'
    # Joining Paths
    Src_File = os.path.join(Temp_Folder,Filename)
    Dst_File = os.path.join(Session_Folder,Filename)

    with open(Src_File,'w') as File :
        ## Creating a file in temp folder
        File.write('ConnMethod=udp\n')
        File.write(f'FriendlyName={Name}@{Domain}\n')
        File.write(f'Host={Host}.{Domain}\n')
        File.write(f'Labels={Domain}\n')

    # Removing the existing file
    if os.path.exists(Dst_File):
        os.remove(Dst_File)
    # Moving created file to destination
    shutil.move(Src_File, Session_Folder)

    return Filename