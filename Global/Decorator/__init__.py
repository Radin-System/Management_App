import tracemalloc
from functools import wraps
from time import perf_counter

def Do_Log (Before = '' , After = '') :
    def Inner (Function) :
        @wraps(Function)
        def Wrapper(*Args , **Kwargs):
            if Before : Args[0].Logger(Before)
            Result = Function(*Args , **Kwargs)
            if After  : Args[0].Logger(After)
            return Result
        return Wrapper
    return Inner

def Do_Performance (Function) :
    @wraps(Function)
    def Wrapper(*Args , **Kwargs):
        tracemalloc.start()
        Start_Time = perf_counter()
        Function(*Args , **Kwargs)
        Current , Peak = tracemalloc.get_traced_memory()
        End_Time = perf_counter()
        print(f'Performance : [StartTime:{Start_Time},MemoryUsage:{Current},Peak:{Peak},EndTime{End_Time}]')
        tracemalloc.stop()
        Result = Function(*Args , **Kwargs)
        return Result
    return Wrapper
