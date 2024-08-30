from typing import Any

class InputField:
    def __init__(self,Type:str,*,
        Label:str = None,
        Description:str = None,
        Placeholder:str = None,
        Wtf_Validators = None,
        ) -> None:
        
        self.Type = Type
        self.Label = Label
        self.Description = Description
        self.Placeholder = Placeholder
        self.WTF_Validators = Wtf_Validators or []

    def __add__(self, Other):
        if not isinstance(Other, InputField):
            raise NotImplementedError('You can only add InputField with each other')

        # Combine lists
        Combined_Validators = self.WTF_Validators + (Other.WTF_Validators or [])
        
        return InputField(
            Type = Other.Type or self.Type,
            Label = Other.Placeholder or self.Label,
            Description = Other.Description or self.Description,
            Placeholder = Other.Placeholder or self.Placeholder,
            Wtf_Validators = Combined_Validators,
        )