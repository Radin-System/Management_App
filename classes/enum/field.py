from enum import Enum

class FieldType(Enum):
    ## String
    Input = 'Input'
    Text = 'Text'
    Username = 'Username'
    Password = 'Password'
    Email = 'Email'
    Color = 'Color'

    ## Integer
    Integer = 'Integer'
    Percent = 'Percent'
    Temp_C = 'Temp_C'
    Temp_F = 'Temp_F'

    ## Bool
    CheckBox = 'CheckBox'

    ## MultiSelect
    Radio = 'Radio'
    DropDown = 'DropDown'

    ## Rel
    Select = 'Select'
    MultiSelect = 'MultiSelect'

    ## DateTime
    Date = 'Date'
    Time = 'Time'
    DateTime = 'DateTime'

    ## File
    FileUpload = 'FileUpload'
    PictureUpload = 'PictureUpload'
    CompactUpload = 'CompactUpload'
    DocUpload = 'DocUpload'
    MusicUpload = 'MusicUpload'