from datetime import datetime

class Task:
    def __init__(
            self, 
            Name : str,
            Action_time:datetime, 
            Timeout:datetime,
            ) -> None:

        self.Name = Name
        self.Action_time = Action_time
        self.Timeout = Timeout

        self.Status = None

    def Action(self) -> None:
        raise NotImplementedError('Please provide an action for the task')

    def Pend(self) -> None:
        self.Status = 'Pending'

    def Complete(self) -> None:
        self.Status = 'Completed'

    def Expire(self) -> None:
        self.Status = 'Expired'

    def Terminate(self) -> None:
        ...

    def Start(self) -> None:
        ...

    def Should_Run(self) -> bool:
        return self.Timeout >= datetime.now() >= self.Action_time

    def Is_Expired(self) -> bool:
        return datetime.now() >= self.Timeout

    def __bool__(self) -> bool:
        return self.Status not in ['Expired','Terminated',None]

    def __str__(self) -> str:
        return f'<Task Name : {self.Name} | Task Status : {self.Status}>'
