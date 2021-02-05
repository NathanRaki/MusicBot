import os
import threading
import tkinter as tk
from logger import Logger
from bot_window import Bot
from PIL import ImageTk, Image

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Login():
	def __init__(self):
		'''This class configures and populates the toplevel window.
		top is the toplevel containing window.'''
		self.logger = ''
		self.logger_cache = ''
		self.top = tk.Tk()
		w = 700
		h = 500
		ws = self.top.winfo_screenwidth()
		hs = self.top.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.top.resizable(False, False)
		self.top.title('Login')
		self.top.configure(background="#000000")
		self.top.configure(highlightcolor="black")
		self.top.attributes("-topmost", True)
		self.top.bind('<Return>', self.check_credentials)

		self.Form = tk.Frame(self.top)
		self.Form.place(relx=0.014, rely=0.02, relheight=0.965, relwidth=0.966)
		self.Form.configure(relief='groove')
		self.Form.configure(relief="groove")
		self.Form.configure(background="#000000")

		self.username_entry = tk.Entry(self.Form)
		self.username_entry.place(relx=0.412, rely=0.407, height=31, relwidth=0.318)
		self.username_entry.configure(background="white")
		self.username_entry.configure(font="TkFixedFont")
		self.username_entry.configure(justify='center')
		self.username_entry.configure(selectbackground="blue")
		self.username_entry.configure(selectforeground="white")

		self.password_entry = tk.Entry(self.Form)
		self.password_entry.place(relx=0.412, rely=0.509, height=31, relwidth=0.318)
		self.password_entry.configure(background="white")
		self.password_entry.configure(font="TkFixedFont")
		self.password_entry.configure(justify='center')
		self.password_entry.configure(selectbackground="blue")
		self.password_entry.configure(selectforeground="white")
		self.password_entry.configure(show="*")

		self.username_label = tk.Label(self.Form)
		self.username_label.place(relx=0.25, rely=0.407, height=33, width=101)
		self.username_label.configure(activebackground="#f9f9f9")
		self.username_label.configure(background="#686868")
		self.username_label.configure(font="-family {Hack} -size 11 -weight bold")
		self.username_label.configure(text='''Username''')

		self.password_label = tk.Label(self.Form)
		self.password_label.place(relx=0.25, rely=0.509, height=33, width=101)
		self.password_label.configure(activebackground="#f9f9f9")
		self.password_label.configure(background="#686868")
		self.password_label.configure(font="-family {Hack} -size 11 -weight bold")
		self.password_label.configure(text='''Password''')

		self.warning_message = tk.Message(self.Form)
		self.warning_message.place(relx=0.279, rely=0.713, relheight=0.118, relwidth=0.441)
		self.warning_message.configure(background="#000000")
		self.warning_message.configure(foreground="#ffffff")
		self.warning_message.configure(justify='center')
		self.warning_message.configure(width=300)

		self.login_button = tk.Button(self.Form)
		self.login_button.place(relx=0.426, rely=0.611, height=33, width=101)
		self.login_button.configure(background="#686868")
		self.login_button.configure(borderwidth="0")
		self.login_button.configure(font="-family {Hack} -size 12 -weight bold")
		self.login_button.configure(highlightthickness="0")
		self.login_button.configure(text='''Login''')
		self.login_button.configure(command=self.check_credentials)
        
	def check_credentials(self, key=''):
		self.warning_message.configure(text='Trying to connect...')
		self.logger = Logger(self.username_entry.get(), self.password_entry.get())
		self.login_thread = threading.Thread(target=self.logger.start)
		self.login_thread.start()
    
	def destroy(self):
		self.login_thread.join()
		self.top.destroy()
		self.top = None

	def refresh(self):
		if self.logger:
			if self.logger_cache != self.logger.success:
				self.logger_cache = self.logger.success
				if self.logger.success == 'yes':
					self.destroy()
					bot = Bot()
					bot.start()
				elif self.logger.success == 'wrong':
					self.warning_message.configure(text='Wrong username OR password.')
			
	def start(self):
		while True:
			try:
				self.top.update_idletasks()
				self.top.update()
				self.refresh()
			except Exception as e:
				print(type(e),':',e)
				break