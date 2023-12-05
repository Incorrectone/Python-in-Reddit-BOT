# Reddit-Python-Execute-BOT

## What this is about?


## So ummmmm API access is gone so lol, but will keep my shit code public still

I am new to Reddit Bots and wanted to create a bot that could execute Python Commands/[Run Saved Functions](/s 'Which would both accept input or not')  
I don't write much in Github pages so I don't know how to source much of this but I will try!	
  
***The bot will only recognise commands from markdown mode.***  
  
***Warning! This bot can extract your accounts password! It has moderator access to the bot account as much as you! You will be basically giving access to anyone who tries execute python! Be carefull.. Even the client secret and ID***
  
This BOT uses [PRAW](https://github.com/praw-dev/praw 'Python Reddit API Wrapper Github') and [mysql-connector](https://dev.mysql.com/doc/connector-python/en/ 'mysql.connector Docs')	
## Details
	
Every Single Screenshot is from [here](https://github.com/Incorrectone/Python-in-Reddit-BOT/blob/main/noworldy.py), [here](https://github.com/Incorrectone/Python-in-Reddit-BOT/blob/main/exec_module.py) and [here](https://github.com/Incorrectone/Python-in-Reddit-BOT/blob/main/MYSQLTables.mysql)	
	
### Setup

![image](https://user-images.githubusercontent.com/71703481/131215522-ebb775a7-e3eb-428a-b19b-76dbdb2e1aaf.png)  
MySQL server Setup  
		
![image](https://user-images.githubusercontent.com/71703481/131216506-5c6e6c2f-7e9c-4ab1-9be7-c0c054b394d5.png)  
Praw Connection Setup  
	
![image](https://user-images.githubusercontent.com/71703481/131216677-ca68e148-33b2-4e80-8239-c8bb503a82e7.png)  
Databases Setup  
	
## Testing/Commands

I took the easy route and used regex to search for commands in reddit comments  

### Looking for the call code

#### [Regex for define/execute Commands:](https://regex101.com/r/wX5QY5/1 'Example')  

```(\$\!(define|execute)\.function\$\n\:(\w{7,20})\:\n\:\n([\S|\s]+)\n\:\n\$\!(mod|user)\.console\.end\$)```  
![image](https://user-images.githubusercontent.com/71703481/131218859-9e14b251-0dc3-4072-9584-88706c230269.png)  
  
  
#### [Regex for search/run Commands:](https://regex101.com/r/Ux9glc/1 'Example')  

```(\$\!(ser|run)\.([\w]{7,20}|all)[\$|\(]([\d|\w| |\,|\']+|)(\)\$|))```  
![image](https://user-images.githubusercontent.com/71703481/131219751-5b8536bc-f244-4210-a29a-731131296927.png)  
  
  
> **The define/execute Function is given priority over search/run Function**
  
### Syntax

Everything other than the explained part is just to add value to the looks and create a syntax which people may not use reguraly and holds no special and meaning/value.  
  
#### define/execute
  
- These commands are only available to the Moderators of a given Subreddit

```python
$!execute.function$
:functionname:
:
def here(x,y):
    return x+y
x=5
y=2
z = 10
print(z*here(x,y))
:
$!mod.console.end$
```  
  
```python
$!define.function$
:functionname:
:
def here(x,y):
    return x+y
x=5
y=2
z = 10
print(z*here(x,y))
:
$!mod.console.end$
```
  
Explanation:  

> $!***execute***.function$  

> $!***define***.function$  
  
- 'execute' helps in identifying the following code is for execution
	- Only one restriction don't end with the *end*...
- 'define' helps in identifying the following code is for saving
	- While saving, code will not be executed.
	- This function has some restrictions which will be discussed later.
  
  
> :***functionname***:  
  
- 'functionname' is the function name that will be stored in the database while saving the code
	- This is only useful in define function.
	- Function name in database is Unique. 
	- While it is required in execute function, it is useless as it is not used (Because I am too lazy and am not making it case specific.)
  
  
> $!***mod***.console.end$  
  
- In this line 'mod' part can be replace with 'user'
- While this too is required in execute function, it is useless as it is not used (Because I am too lazy and am not making it case specific.)
- In define function however:
	- This line defines what the permissions of a saved function should be, when called the code checks if it is allowed to be executed by a 'Normal User' or a 'Moderator.'
  
  
#### search/run
  
```
$!ser.functi2onname$
```
```
$!run.functi2onname(1,5)$
$!run.functi2onname$
```
  
- Pretty self explanatory
- For the search function:
	- No need for any Input only function name is needed
	- Output -> check Output section
- For the run function:
	- May or may not need Input
	- For knowledge use search function
  
  
### Output
  
![screencapture-github-Incorrectone-Reddit-Python-Execute-BOT-edit-main-README-md-2021-08-28-19_20_40](https://user-images.githubusercontent.com/71703481/131220199-e1b73768-4701-4a37-a6c1-ec5c2b4ad848.png)  
Main Output List  
  
#### For execute command:

Everything in that will be shown in the output will be the print function. As seen in the second python file:
- It records every single thing printed and then replies to the comment with that.
- Any error will be reported in the comment if it occurs.
- Everything done is recorded in the second table, This is for bug checking.
  
##### Example:  
- Without Error:  
	![image](https://user-images.githubusercontent.com/71703481/131220580-25ad975f-5119-4cdf-bc8b-a08cf69cf1a7.png)  
- With Error:  
	![image](https://user-images.githubusercontent.com/71703481/131220683-c836506d-1870-483e-beb8-baf842a3fb86.png)
  
#### For define command:

- Only confirmation whether the new function has been stored
	- Shows the error(outside of the code) if occurs.
	- Will not even check whether the code is wrong or not.
  
##### Example:  
- If the name is available:  
	![image](https://user-images.githubusercontent.com/71703481/131220842-b0df5ba1-8df7-4400-a0af-e59eaab1cd44.png)
- If the name is not available:  
	![image](https://user-images.githubusercontent.com/71703481/131220894-7f7bcfbe-876c-4ff4-85e5-28bb2f451f97.png)
  
#### For search command:

- Outputs will be:  
	![image](https://user-images.githubusercontent.com/71703481/131220392-7608d526-245d-4af8-8eb1-3adc70f9e10d.png)
   
##### Example
![image](https://user-images.githubusercontent.com/71703481/131221006-b1a45ca3-214d-4fa8-98fb-c52394e63109.png)  
  	
  
### Meanwhile in Log:
![image](https://user-images.githubusercontent.com/71703481/131221109-40c82acf-a7b6-4623-a040-e8cd1d413c0a.png)  
> In localhost/phpmyadmin/
  

### Input

- The execute function does not have any restrictions in the general sense
	- Just don't use the end phrase anywhere other than at the end (:p)
  
- The define function does have other wise it will not work
	- Don't use the phrase 
		> \^\^\^INPUT\^\^\^
	- Since the define command is not executed upon saving this will not show up an error
	- No use of %s formating in functions where input is to be taken! Otherwise it is fine!
  
```
$!run.functioname(1,2)$
```
- The run function just need to have
	- This part is enough to have '([Value],[Value])' for Inputing
	- If there are no inputs, Don't put it!
  
##### Example:

- Defining  
	![image](https://user-images.githubusercontent.com/71703481/131223501-b643eec2-d8b2-48c0-850a-911a01f75875.png)  
  
	![image](https://user-images.githubusercontent.com/71703481/131223538-a793cd90-6ae8-4f7d-9b09-2e41b9df4ddf.png)  
	
	```python
	$!define.function$
	:functionname4:
	:
	def here(x,y):
	    return x+y
	x=^^^INPUT^^^
	y= ^^^INPUT^^^
	z = 10
	print(z*here(x,y))
	:
	$!mod.console.end$
	```
  
- Executing  
	![image](https://user-images.githubusercontent.com/71703481/131223514-a67f8de5-dd56-47f9-93ab-482a9a2797f0.png)  


