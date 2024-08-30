import enum

class FieldTypeEnum(enum):
    ## String
    Input = 'Input'
    Text = 'Text'
    Username = 'Username'
    Password = 'Password'
    Email = 'Email'
    Color = 'Color'

    ## DateTime
    Date = 'Date'
    Time = 'Time'
    DateTime = 'DateTime'

    ## Integer
    Integer = 'Integer'
    Percent = 'Percent'
    Temp_C = 'Temp_C'
    Temp_F = 'Temp_F'

    ## File
    FileUpload = 'FileUpload'
    PictureUpload = 'PictureUpload'
    CompactUpload = 'CompactUpload'
    DocUpload = 'DocUpload'
    MusicUpload = 'MusicUpload'