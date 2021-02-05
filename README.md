# MusicBot
 
### This bot was made in a learning purpose and not for real use.
### I created it as a first Browser Automation application, Napster does not want
### you to use a bot to listen music so don't.

## Install requirements :
```shell
python -m pip install -r requirements.txt
```

## Compile to exe :
```shell
pip install pyinstaller
pyinstaller main.spec
```

## Execute with python :
```shell
python main.py
```

## Log to the application :
Username : admin
Password : 1234
(You can change these in the logger.py file)

## How to use :
You are supposed to have three txt files :  
-> An accounts file that contains your Napster accounts credentials in this format : mail:password  
-> A proxies file with proxies ip and port for each Napster account : ip:port[:username:password]  
-> An urls file with the musics you want to stream  
Once you've entered these files in the application, just hit Start and the bot begins his magic.