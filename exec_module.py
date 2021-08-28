import sys
import io

global _output_
global _exception_
_mmsg_ = '''
### ***An exception has been raised:***   
    
{}  
  
>Please check whether you used the correct version of python   
>in which your code is being executed [PYTHON 3.7.9](https://www.python.org/downloads/release/python-379/)  
>Please check whether you are using the correct imported modules  
>Please recheck your code for bugs!  
   
>If There are None in your code and the message still appears     
>__Please message the DEVS for potential bugs!__  
    
'''

_var_list_= ['_all_vars_','_var_name_','_var_list_','_output_', '_exception_', '_mmsg_', 'execcode', 'old_stdout', 'new_stdout', '_tick_', '_extract_group_list_']

def execcode(_extract_group_list_):
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    global _tick_

    try: 
        exec(_extract_group_list_)
        _output_ = new_stdout.getvalue()
        _tick_ = None
    except Exception as _exception_:
        _output_ = _mmsg_.format(_exception_)
        _tick_ = _exception_

    sys.stdout = old_stdout

    _all_vars_ = dir()
    for _var_name_ in _all_vars_:
        if not _var_name_.startswith('__') and _var_name_ not in _var_list_:
            exec('del {}'.format(_var_name_))
    
    return _output_, _tick_

