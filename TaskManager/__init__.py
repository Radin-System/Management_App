import time
import threading
import multiprocessing
from datetime     import datetime, timedelta
from Class.Class import Component

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

        self.Args = ()
        self.KWargs = {}
        self.Action = None
        self.Process = None
        self.Status = None

    def Delay_Action(self,Added_Time : timedelta) -> None:
        self.Action_time += Added_Time

    def Delay_Timeout(self,Added_Timeout : timedelta) -> None:
        self.Timeout += Added_Timeout

    def Set_Action(self, Action, *Args, **KWargs) -> None:
        self.Args = Args
        self.KWargs = KWargs
        self.Action = Action
        self.Status = 'Ready'

    def Pend(self) -> None:
        self.Status = 'Pending'

    def Complete(self) -> None:
        self.Status = 'Completed'

    def Expire(self) -> None:
        self.Status = 'Expired'

    def Terminate(self) -> None:
        if self.Process and self.Process.is_alive():
            self.Process.terminate()
            self.Process.join()
            self.Status = 'Terminated'

    def Start(self) -> None:
        if self.Action:
            self.Process = multiprocessing.Process(target=self.Action, args=self.Args, kwargs=self.KWargs)
            self.Process.start()
            self.Status = 'Started'

    def Should_Run(self) -> bool:
        return self.Timeout >= datetime.now() >= self.Action_time

    def Is_Expired(self) -> bool:
        return datetime.now() >= self.Timeout

    def __bool__(self) -> bool:
        return self.Status not in ['Expired','Terminated',None]

    def __str__(self) -> str:
        return f'<Task Name : {self.Name} | Task Status : {self.Status}>'

class SimpleTaskManager(Component):
    def __init__(self, Name:str, *,
            Check_Interval:int|float
            ) -> None:
        
        self.Name = Name
        self.Check_Interval = Check_Interval
        
        self.Tasks : list[Task] = []
        self.Thread = threading.Thread(target=self.Main_Loop)

    def Add(self, Task: Task) -> None:
        Task.Pend()
        self.Tasks.append(Task)

    def Remove(self, Task: Task) -> None:
        if Task in self.Tasks:
            self.Tasks.remove(Task)

    def Check_Tasks(self) -> None:
        for Current_Task in self.Tasks:
            if Current_Task.Process :
                if Current_Task.Process.is_alive():
                    if Current_Task.Is_Expired():
                        Current_Task.Terminate()
                        self.Remove(Current_Task)
                    elif Current_Task.Should_Run():
                        continue
                else :
                    Current_Task.Complete()
                    self.Remove(Current_Task)
            else :
                if Current_Task.Is_Expired():
                    Current_Task.Expire()
                    self.Remove(Current_Task)
                elif Current_Task.Should_Run(): 
                    Current_Task.Start()
                    self.Remove(Current_Task)

    def Main_Loop(self) -> None:
        while self.Running:
            self.Check_Tasks()
            time.sleep(self.Check_Interval)

    def Start_Actions(self) -> None:
        self.Thread.start()

    def Stop_Actions(self) -> None:
        self.Thread.join()