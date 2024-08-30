from typing import Any

class InputField:
    def __init__(self,Type:str,*,
        Label:str = None,
        Description:str = None,
        Placeholder:str = None,
        Value:str = None,
        Wtf_Validators = None,
        **KWargs,
        ) -> None:
        
        self.Type = Type
        self.Label = Label
        self.Description = Description
        self.Placeholder = Placeholder
        self.Value = Value
        self.WTF_Validators = Wtf_Validators or []
        self.Extra = KWargs
