import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from login_window import Login
from bot_window import Bot

if __name__ == '__main__':
	bot = Bot()
	bot.start()