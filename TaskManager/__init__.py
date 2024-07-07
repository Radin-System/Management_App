from Global import Main_Config
from .Class import SimpleTaskManager

TaskManager = SimpleTaskManager('TaskManager',
    Check_Interval = Main_Config.Get('TASKMANAGER','chck_interval'),
    )
