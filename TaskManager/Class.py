import time
import threading
import multiprocessing
from datetime import datetime, timedelta

class Task:
    def __init__(
            self, 
            Name : str,
            Action_time = datetime.now() , 
            Timeout = datetime.now() + timedelta(days=365)
            ) -> None:
        
        self.Name = Name
        self.Action_time = Action_time
        self.Timeout = Timeout

        self.Args = ()
        self.KWargs = {}
        self.Action = None
        self.Process = None
        self.Status = None

    def Set_Action(self, Action, *Args, **KWargs) -> None:
        self.Args = Args
        self.KWargs = KWargs
        self.Action = Action
        self.Status = 'Set'

    def Delay_Action(self,Added_Time : timedelta) -> None:
        self.Action_time += Added_Time

    def Delay_Timeout(self,Added_Timeout : timedelta) -> None:
        self.Timeout += Added_Timeout

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

    def __str__(self) -> str:
        return f'<Task Name : {self.Name} | Task Status : {self.Status}>'

class TaskManager:
    def __init__(self) -> None:
        self.Tasks : list[Task] = []
        self.Running = False
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
            time.sleep(1)

    def Start(self) -> None:
        if not self.Running:
            self.Running = True
            self.Thread.start()

    def Stop(self) -> None:
        if self.Running:
            self.Running = False
            self.Thread.join()