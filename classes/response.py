from flask import jsonify

class Response:
    def __init__(self,Message:dict|str,*,
        Status:str='Response',
        Code:int=200,
        **KWargs,
        ) -> None:
        
        self.Message = Message
        self.Status = Status
        self.Code = Code
        self.Kwargs = KWargs
    
    def Jsonify_Response(self) -> None:
        Data = dict(**self.Kwargs)
        Data['message'] = self.Message
        Data['status'] = self.Status
        Data['code'] = self.Code
        
        return jsonify(Data)