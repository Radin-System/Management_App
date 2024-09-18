from sqlalchemy import Column
from wtforms import (
    RadioField,
    SelectField,
    StringField,
    IntegerField,
    BooleanField,
    DateTimeField,
    PasswordField,
    ColorField,
    FileField,
    TextAreaField,
    #MultipleChoiceField,
    )
from wtforms.validators import DataRequired, Email

from classes.enum import FieldType
from classes.field.input import InputField
from classes.policy.input import InputPolicy


ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Create_API_Response(Message:dict|str, Status:str='Response', Code:int=200, **KWargs) -> dict:
    # Creating Base Response
    API_Response = dict(**KWargs)

    API_Response['status'] = Status
    API_Response['message'] = Message
    API_Response['code'] = Code

    return API_Response

def Create_Flask_WTF_Field(Column):
    Policy: InputPolicy = Column.info.get('Policy')
    Field: InputField = Column.info.get('Field')

    if not Policy or not Field:
        raise ValueError(f"Missing Policy or Field info in column: {Column.name}")

    is_readonly = not Policy.Changeable
    is_visible = Policy.Visible

    field_args = {
        'label': Field.Label or Column.name.capitalize(),
        'description': Field.Description or '',
        'default': Column.default.arg if Column.default is not None else None,
        'render_kw': {
            'placeholder': Field.Placeholder or '',
            'readonly': 'readonly' if is_readonly else '',
            'style': 'display:none;' if not is_visible else ''
        }
    }

    # Determine validators
    validators = []
    if not Column.nullable:
        validators.append(DataRequired())
    if Field.Type == FieldType.Email.value:
        validators.append(Email())

    validators.extend(Field.WTF_Validators)
    validators.extend(Policy.Validators)
    
    field_args['validators'] = validators

    # Map field type to WTForms field
    if Field.Type == FieldType.Input.value:
        return StringField(**field_args)

    elif Field.Type == FieldType.Text.value:
        return TextAreaField(**field_args)

    elif Field.Type == FieldType.Username.value:
        return StringField(**field_args)

    elif Field.Type == FieldType.Password.value:
        return PasswordField(**field_args)

    elif Field.Type == FieldType.Email.value:
        return StringField(**field_args)

    elif Field.Type == FieldType.Color.value:
        return ColorField(**field_args)

    elif Field.Type == FieldType.Date.value:
        return DateTimeField(format='%Y-%m-%d', **field_args)

    elif Field.Type == FieldType.Time.value:
        return DateTimeField(format='%H:%M:%S', **field_args)

    elif Field.Type == FieldType.DateTime.value:
        return DateTimeField(format='%Y-%m-%d %H:%M:%S', **field_args)

    elif Field.Type == FieldType.Integer.value:
        return IntegerField(**field_args)

    elif Field.Type == FieldType.Percent.value:
        return IntegerField(**field_args)  # Add specific validation for percentage if needed

    elif Field.Type == FieldType.Temp_C.value:
        return IntegerField(**field_args)  # Add specific validation for temperature in Celsius if needed

    elif Field.Type == FieldType.Temp_F.value:
        return IntegerField(**field_args)  # Add specific validation for temperature in Fahrenheit if needed

    elif Field.Type == FieldType.CheckBox.value:
        return BooleanField(**field_args)

    elif Field.Type == FieldType.Radio.value:
        choices = Field.Value if Field.Value else []
        return RadioField(**field_args, choices=choices)

    elif Field.Type == FieldType.DropDown.value:
        choices = Field.Value if Field.Value else []
        return SelectField(**field_args, choices=choices)

    elif Field.Type == FieldType.Select.value:
        choices = Field.Value if Field.Value else []
        return SelectField(**field_args, choices=choices)

    #elif Field.Type == FieldType.MultiSelect.value:
    #    choices = Field.Value if Field.Value else []
    #    return MultipleChoiceField(**field_args, choices=choices)

    elif Field.Type in [FieldType.FileUpload.value, FieldType.PictureUpload.value, FieldType.CompactUpload.value, FieldType.DocUpload.value, FieldType.MusicUpload.value]:
        return FileField(**field_args)  # Adjust as needed for specific file types

    else:
        raise ValueError(f"Unsupported field type: {Field.Type}")
