class Validator:
    def __new__(cls, Input:str):
        Instance = super().__new__(cls)
        Instance.Input = Input
        Instance.Error_Message = 'Something went wrong while validating the input'
        Instance.Check_For_Error()
        return Instance.Input

    def Check_For_Error(self) -> None:
        if not self.Validate():
            raise ValueError(self.Error_Message)

    def Validate(self) -> bool:
        raise NotImplementedError('Subclasses should implement this method.')