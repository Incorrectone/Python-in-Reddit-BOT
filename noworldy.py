import re
import praw
import exec_module
from praw import reddit
from praw.reddit import Comment, Subreddit
import mysql.connector as mysql

_mydb_ = mysql.connect(
  host="localhost",
  user="user",
  password="password",
  database="database"
)

_reddit_ = praw.Reddit(client_id = "client_id",
                     client_secret = "client_secret",
                     username = "username",
                     password =  "password",
                     user_agent = "user_agent")

_subreddit_ = _reddit_.subreddit('myservers')
_cursor_ = _mydb_.cursor()
_dict_cmmd_hardcoded_ = {'execute':'_exec_cmmd_found_',
                         'define':'_def_cmmd_found_',
                         'ser':'_search_func_', 
                         'run':'_run_saved_'}
_moderators_ = [x.name for x in _subreddit_.moderator()]

_custom_reply_list_ = ['''
### ***You do not have the Permissions to use this command***   
---   
>Your Actions have been recorded in a log for future reference  

>If you think this a mistake! **Please contact the moderators!**   
---
^(Beep Boop This Message is done by a [BOT](https://reddit.com/r/myservers))
''',
'''
### **Execution Done**
  
>Your Actions have been recorded in a log for future reference
  

**Results**    

---      
  
{}
    
---    
    
^(Beep Boop This Message is done by a [BOT](https://reddit.com/r/myservers))
''',
'''
***An exception has been raised:***   
    
{}  
  
>The code that was to be stored has not been executed/Stored in the database!  
>If it is a duplicate name Exception, Please try with another name  
>If anything else your code may have errors  
   
>If There are None in your code and the message still appears     
>__Please message the DEVS for potential bugs!__    
''',
'''
### **Some ERROR HAPPENED**
  
>This Action has been recorded in a log for future reference
>No need to report this!

^(Beep Boop This Message is done by a [BOT](https://reddit.com/r/myservers))
''']

def _unpack_essentials_(_reclass_extracted_):
    _extract_group_list_ = list(_reclass_extracted_.group(1,2,3,4,5))
    return _extract_group_list_

def _input_check_(_extract_group_list_):
    x = _extract_group_list_[3].find('^^^INPUT^^^')
    if x == -1:
        return 'False'
    else:
        return 'True'

def _exec_cmmd_found_(_comment_, _extract_group_list_):
    _output_exec_cmmd_, _exception_ = exec_module.execcode(_extract_group_list_[3])
    global _log_success_reason_
    if _exception_ == None and _extract_group_list_[0] != 'RUN':
        _comment_.reply(_custom_reply_list_[1].format(_output_exec_cmmd_))
        _log_success_reason_ = 'Execute | Success' 
    elif _exception_ == None and _extract_group_list_[0] == 'RUN':
        _comment_.reply(_custom_reply_list_[1].format(_output_exec_cmmd_))
        _log_success_reason_ = 'Run | Success | {}'.format(_extract_group_list_[1])
    else:
        _comment_.reply(_custom_reply_list_[1].format(_output_exec_cmmd_))
        _log_success_reason_ = _exception_

def _def_cmmd_found_(_comment_, _extract_group_list_):
    _sql_cmmd_ = "INSERT INTO defined_functions (Function_name , Comment_ID, DateandTime, Author, Execution, Input, Perm) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    _log_val_ = (_extract_group_list_[2], _comment_.id, str(_comment_.created_utc) , str(_comment_.author), _extract_group_list_[3], _input_check_(_extract_group_list_), _extract_group_list_[4])
    global _log_success_reason_
    try:
        _cursor_.execute(_sql_cmmd_, _log_val_)
        _mydb_.commit()
        _log_success_reason_ = 'Define | Success'
        _comment_.reply(_custom_reply_list_[1].format('Your {} has been put into the database!'.format(_extract_group_list_[2])))
    except Exception as _exception_:
        _log_success_reason_ = _exception_
        _comment_.reply(_custom_reply_list_[1].format(eval('_custom_reply_list_[2]').format(str(_log_success_reason_))))

def _run_saved_(_comment_, _extract_group_list_):
    _cursor_.execute("SELECT * FROM defined_functions")
    _dat_in_bw_ = _cursor_.fetchall()
    _list_pre_func_ = [x[1] for x in _dat_in_bw_]
    _list_pre_exec_ = [x[5] for x in _dat_in_bw_]
    _list_pre_input_ = [x[6] for x in _dat_in_bw_]
    _list_pre_Perms_ = [x[7] for x in _dat_in_bw_]
    _index_ = _list_pre_func_.index(_extract_group_list_[2])
    global _log_success_reason_


    if _extract_group_list_[2] in _list_pre_func_:
        
        if _comment_.author in _moderators_ and _list_pre_Perms_[_index_] == 'mod':
            if _list_pre_input_[_index_] == 'True':
                try:
                    _exec_cmmd_ = _list_pre_exec_[_index_]
                    _exec_cmmd_ = _exec_cmmd_.replace("^^^INPUT^^^", "%s")
                    _exec_cmmd_found_(_comment_, ['RUN','Mod','',_exec_cmmd_ % tuple(_extract_group_list_[3].split(','))])
                except Exception as e:
                    _log_success_reason_ = e
                    _comment_.reply(_custom_reply_list_[1].format(eval('_custom_reply_list_[2]').format(str(_log_success_reason_))))
            elif _list_pre_input_[_index_] == 'False':
                _exec_cmmd_ = _list_pre_exec_[_index_]
                _exec_cmmd_found_(_comment_, ['RUN','Mod','',_exec_cmmd_])
        
        elif _list_pre_Perms_[_index_] == 'user':
            if _list_pre_input_[_index_] == 'True':
                try:
                    _exec_cmmd_ = _list_pre_exec_[_index_]
                    _exec_cmmd_ = _exec_cmmd_.replace("^^^INPUT^^^", "%s")
                    _exec_cmmd_found_(_comment_, ['RUN','Mod','',_exec_cmmd_ % tuple(_extract_group_list_[3].split(','))])
                except Exception as e:
                    _log_success_reason_ = e
                    _comment_.reply(_custom_reply_list_[1].format(eval('_custom_reply_list_[2]').format(str(_log_success_reason_))))
            elif _list_pre_input_[_index_] == 'False':
                _exec_cmmd_ = _list_pre_exec_[_index_]
                _exec_cmmd_found_(_comment_, ['RUN','Mod','',_exec_cmmd_])
        
        elif _comment_.author not in _moderators_ and _list_pre_Perms_[_index_] == 'mod':
            _comment_.reply(_custom_reply_list_[0])
            _log_success_reason_ = 'Not enough Perms | Run'
        
        else:
            _comment_.reply(_custom_reply_list_[3])
            _log_success_reason_ = 'Not enough Perms | Run'
    
    else:
        pass

def _search_func_(_comment_, _extract_group_list_):
    _cursor_.execute("SELECT * FROM defined_functions")
    _dat_in_bw_ = _cursor_.fetchall()
    _index_ = -1
    _Perms_ = 'Not Found'
    _Input_ = 'Not Found'
    _found_ = False
    for x in range(0,len(_dat_in_bw_)):
        if _extract_group_list_[2] == _dat_in_bw_[x][1]:
            _index_ = x
            _found_ = True
            _Perms_ = _dat_in_bw_[x][7]
            _Input_ = _dat_in_bw_[x][6]
            pass
    
    _comment_.reply(_custom_reply_list_[1].format('''Found: {}    
    Input: {}    
    Perms: {}'''.format(_found_, _Input_, _Perms_)))

    global _log_success_reason_
    _log_success_reason_ = "Search | {}".format(_extract_group_list_[2])

def _record_log_(_comment_, _reclass_extracted_):
    _sql_cmmd_ = "INSERT INTO log_changes (Author, Comment_ID, DateandTime, Content, Reason, Success) VALUES (%s, %s, %s, %s, %s, %s)"
    _log_val_ = (str(_comment_.author), _comment_.id, str(_comment_.created_utc) , _reclass_extracted_.group(0), _reclass_extracted_.group(1), str(_log_success_reason_))
    _cursor_.execute(_sql_cmmd_, _log_val_)
    _mydb_.commit()

def _index_cmmd_hardcoded_(_comment_, _extract_group_list_):
    if _extract_group_list_[1] == 'define' or _extract_group_list_[1] == 'execute' or _extract_group_list_[1] == 'run' or _extract_group_list_[1] == 'ser':
        if _comment_.author in _moderators_:
            _function_chosen_ = _dict_cmmd_hardcoded_[_extract_group_list_[1]]
            exec('{}(_reddit_.comment(id=\'{}\'),{})'.format(_function_chosen_ ,_comment_, _extract_group_list_)) # problem here _comment_ class converts to __comment__.id
        else:
            _comment_.reply(_custom_reply_list_[0])

for _comment_ in _subreddit_.stream.comments(skip_existing=True):
    print('Comment ID:', _comment_.id)
    _reclass_extracted_ = re.search('(\$\!(define|execute)\.function\$\n\:(\w{7,20})\:\n\:\n([\S|\s]+)\n\:\n\$\!(mod|user)\.console\.end\$)', 
    _comment_.body)
    if _reclass_extracted_:
        pass
    else:
        _reclass_extracted_ = re.search('(\$\!(ser|run)\.([\w]{7,20}|all)[\$|\(]([\d|\w| |\,|\']+|)(\)\$|))', _comment_.body)
    
    if _reclass_extracted_:
        _index_cmmd_hardcoded_(_comment_, _unpack_essentials_(_reclass_extracted_))
        _record_log_(_comment_, _reclass_extracted_)
    else:
        pass
