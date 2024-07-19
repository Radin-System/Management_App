import tracemalloc
from functools import wraps
from time import perf_counter
from typing import Callable

def Return_False_On_Exception(Function) -> Callable:
    @wraps(Function)
    def Wrapper(*Args, **Kwargs):
        try : return Function(*Args, **Kwargs)
        except : return False
    return Wrapper

def Do_Log(Before:str = '', After:str = '') -> Callable:
    def Inner (Function):
        @wraps(Function)
        def Wrapper(*Args, **Kwargs):
            if Before : Args[0].Logger(Before)
            Result = Function(*Args , **Kwargs)
            if After : Args[0].Logger(After)
            return Result
        return Wrapper
    return Inner

def Running_Required(Function) -> callable :
    @wraps(Function)
    def Wrapper(*Args, **Kwargs):
        if not Args[0].Is_Running(): raise Exception(f'The component must be started to preform this action<{Function.__name__}>')
        Result = Function(*Args, **Kwargs)
        return Result
    return Wrapper

def Connection_Required(Function) -> callable :
    @wraps(Function)
    def Wrapper(*Args, **Kwargs):
        if not Args[0].Is_Connected(): raise ConnectionError(f'no connection to preform this action <{Function.__name__}>')
        Result = Function(*Args, **Kwargs)
        return Result
    return Wrapper

def Do_Performance (Function) -> Callable:
    @wraps(Function)
    def Wrapper(*Args, **Kwargs):
        tracemalloc.start()
        Start_Time = perf_counter()
        Function(*Args, **Kwargs)
        Current, Peak = tracemalloc.get_traced_memory()
        End_Time = perf_counter()
        print(f'Performance : [StartTime:{Start_Time},MemoryUsage:{Current},Peak:{Peak},EndTime{End_Time}]')
        tracemalloc.stop()
        Result = Function(*Args, **Kwargs)
        return Result
    return Wrapper