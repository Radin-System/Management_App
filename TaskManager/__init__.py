from Global import Main_Config
from .Class import SimpleTaskManager

TaskManager = SimpleTaskManager('Task Manager',
    Check_Interval = Main_Config.Get('TASKMANAGER','chck_interval'),
    )
