import time
import threading
from Class.component import Component
from Class.task import Task

class TaskManager(Component):
    def __init__(self,*,
            Check_Interval:int|float
            ) -> None:

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