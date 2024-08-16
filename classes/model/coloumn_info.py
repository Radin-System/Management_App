class Coloumn_Info:
    def __init__(self,*,
        Validators:list=None,
        Convertors:list=None,
        Changeable:bool=True,
        Hidden:bool=False,
        Field_Type:str=None,
        ) -> None:
        
        self.Validators = Validators or []
        self.Convertors = Convertors or []
        self.Changeable = Changeable
        self.Hidden = Hidden
        self.Field_Type = Field_Type

    def __add__(self, Other):
        if not isinstance(Other, Coloumn_Info):
            return NotImplemented

        # Combine lists
        combined_validators = self.Validators + (Other.Validators or [])
        combined_convertors = self.Convertors + (Other.Convertors or [])

        # Override strings
        combined_field_type = Other.Field_Type if Other.Field_Type is not None else self.Field_Type

        # Combine booleans with the custom logic
        combined_changeable = self._combine_bools(self.Changeable, Other.Changeable)
        combined_hidden = self._combine_bools(self.Hidden, Other.Hidden)

        return Coloumn_Info(
            Validators=combined_validators,
            Convertors=combined_convertors,
            Changeable=combined_changeable,
            Hidden=combined_hidden,
            Field_Type=combined_field_type
        )

    @staticmethod
    def _combine_bools(first, second):
        if first is None: return second
        if second is None: return first
        return first or second

    def Calc_Dict(self) -> dict:
        return {
            'Setattar': {
                'Validators':self.Validators,
                'Convertors':self.Convertors,
                },
            'Flags':{
                'Hidden':self.Hidden,
                'Changeable':self.Changeable,
                },
            'Field':{
                'Type':self.Field_Type,
            },
        }
