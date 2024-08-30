from typing import Any

class InputPolicy:
    def __init__(self,Name:str,*,
        Validators:list=None,
        Convertors:list=None,
        Changeable:bool=None,
        Visible:bool=None,
        First_Convert:bool=None,
        ) -> None:

        self.Name = Name
        self.Validators = Validators or []
        self.Convertors = Convertors or []
        self.Changeable = Changeable
        self.Visible = Visible
        self.First_Convert = First_Convert

    def __add__(self, Other):
        if not isinstance(Other, InputPolicy):
            raise NotImplementedError('You can only add ColumnPolicy with each other')

        # Combine lists
        Combined_Validators = self.Validators + (Other.Validators or [])
        Combined_Convertors = self.Convertors + (Other.Convertors or [])

        # Combine booleans with the custom logic
        Combined_Changeable = self._combine_bools(self.Changeable, Other.Changeable)
        Combined_Visible = self._combine_bools(self.Visible, Other.Visible)
        Combined_First_Convert = self._combine_bools(self.First_Convert, Other.First_Convert)

        return InputPolicy(
            Name = Other.Name,
            Validators = Combined_Validators,
            Convertors = Combined_Convertors,
            Changeable = Combined_Changeable,
            Visible = Combined_Visible,
            First_Convert = Combined_First_Convert,
        )

    @staticmethod
    def _combine_bools(First:bool|None, Second:bool|None) -> bool:
        if Second is None: 
            return First
        return Second

    def Apply(self, Input:Any) -> Any:

        if self.First_Convert:
            for Convertor in self.Convertors:
                Input = Convertor(Input)

            for Validator in self.Validators:
                Validator(Input)

        else:
            for Validator in self.Validators:
                Validator(Input)

            for Convertor in self.Convertors:
                Input = Convertor(Input)

        return Input