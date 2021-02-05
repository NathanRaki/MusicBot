import os
import sys
import scroll
import threading
import methods as nm
import tkinter as tk
from bot import NapsterBot
from functools import partial
from tkinter import filedialog

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class PrintLogger():
	def __init__(self, textbox):
		self.textbox = textbox
	def write(self, text):
		self.textbox.insert(tk.END, text)
	def flush(self):
		pass

class Bot():
    
	def __init__(self):
		try:
			self.save = nm.load('save')
		except:
			self.save = {'streams':0, 'earnings':0}
			nm.save(self.save, 'save')
		self.napsterbot = ''
		self.accounts_path = ''
		self.proxies_path = ''
		self.tracks_path = ''
		self.threads = 0
		self.streams = 0
		self.earnings = 0

		self.top = tk.Tk()
		w = 700
		h = 500
		ws = self.top.winfo_screenwidth()
		hs = self.top.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.top.resizable(True, False)
		self.top.minsize(w,h)
		self.top.maxsize(w+200,h)
		self.top.title('Omega Napster')
		self.top.configure(background="#2d2d2d")
		self.top.attributes("-topmost", True)

		# Frame Principale
		self.Frm_Main = tk.Frame(self.top)
		self.Frm_Main.place(relx=0.0, rely=-0.02, relheight=0.99, relwidth=0.994)
		self.Frm_Main.configure(relief="groove")
		self.Frm_Main.configure(background="#2d2d2d")

		# Frame Haut-Gauche
		self.Frm_UpLeft = tk.Frame(self.Frm_Main)
		self.Frm_UpLeft.place(relx=0.029, rely=0.04, relheight=0.303, relwidth=0.481)

		self.Frm_UpLeft.configure(relief='ridge')
		self.Frm_UpLeft.configure(borderwidth="3")
		self.Frm_UpLeft.configure(relief="ridge")
		self.Frm_UpLeft.configure(background="#1b1b1b")
		self.Frm_UpLeft.configure(highlightbackground="#000000")
		self.Frm_UpLeft.configure(highlightcolor="#000000")

		self.Lbl_Accounts = tk.Label(self.Frm_UpLeft)
		self.Lbl_Accounts.place(relx=0.06, rely=0.133, height=29, width=90)
		self.Lbl_Accounts.configure(activebackground="#ffffff")
		self.Lbl_Accounts.configure(activeforeground="black")
		self.Lbl_Accounts.configure(anchor='n')
		self.Lbl_Accounts.configure(background="#3f3f3f")
		self.Lbl_Accounts.configure(disabledforeground="#a3a3a3")
		self.Lbl_Accounts.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Accounts.configure(foreground="#ffffff")
		self.Lbl_Accounts.configure(highlightbackground="#d9d9d9")
		self.Lbl_Accounts.configure(highlightcolor="black")
		self.Lbl_Accounts.configure(relief="ridge")
		self.Lbl_Accounts.configure(text='''Accounts:''')

		self.Lbl_Accounts_File = tk.Label(self.Frm_UpLeft)
		self.Lbl_Accounts_File.place(relx=0.328, rely=0.147, height=25, width=120)
		self.Lbl_Accounts_File.configure(activebackground="#f9f9f9")
		self.Lbl_Accounts_File.configure(activeforeground="black")
		self.Lbl_Accounts_File.configure(background="#e6e6e6")
		self.Lbl_Accounts_File.configure(borderwidth="0")
		self.Lbl_Accounts_File.configure(disabledforeground="#a3a3a3")
		self.Lbl_Accounts_File.configure(font="-family {Calibri} -size 10")
		self.Lbl_Accounts_File.configure(foreground="#000000")
		self.Lbl_Accounts_File.configure(highlightbackground="#d9d9d9")
		self.Lbl_Accounts_File.configure(highlightcolor="black")
		self.Lbl_Accounts_File.configure(relief="ridge")
		self.Lbl_Accounts_File.configure(text='None')

		self.Btn_Accounts = tk.Button(self.Frm_UpLeft)
		self.Btn_Accounts.place(relx=0.716, rely=0.14, height=25, width=70)
		self.Btn_Accounts.configure(activebackground="#ececec")
		self.Btn_Accounts.configure(activeforeground="#000000")
		self.Btn_Accounts.configure(anchor='n')
		self.Btn_Accounts.configure(background="#3f3f3f")
		self.Btn_Accounts.configure(disabledforeground="#a3a3a3")
		self.Btn_Accounts.configure(font="-family {Calibri} -size 10 -weight bold -underline 1")
		self.Btn_Accounts.configure(foreground="#ffffff")
		self.Btn_Accounts.configure(highlightbackground="#d9d9d9")
		self.Btn_Accounts.configure(highlightcolor="black")
		self.Btn_Accounts.configure(pady="0")
		self.Btn_Accounts.configure(relief="groove")
		self.Btn_Accounts.configure(text='''Browse''')
		self.Btn_Accounts.configure(command=partial(self.browseFiles, 'accounts'))

		self.Lbl_Proxies = tk.Label(self.Frm_UpLeft)
		self.Lbl_Proxies.place(relx=0.06, rely=0.4, height=29, width=90)
		self.Lbl_Proxies.configure(activebackground="#ffffff")
		self.Lbl_Proxies.configure(activeforeground="black")
		self.Lbl_Proxies.configure(anchor='n')
		self.Lbl_Proxies.configure(background="#3f3f3f")
		self.Lbl_Proxies.configure(disabledforeground="#a3a3a3")
		self.Lbl_Proxies.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Proxies.configure(foreground="#ffffff")
		self.Lbl_Proxies.configure(highlightbackground="#d9d9d9")
		self.Lbl_Proxies.configure(highlightcolor="black")
		self.Lbl_Proxies.configure(relief="ridge")
		self.Lbl_Proxies.configure(text='''Proxies:''')

		self.Lbl_Proxies_File = tk.Label(self.Frm_UpLeft)
		self.Lbl_Proxies_File.place(relx=0.328, rely=0.407, height=25, width=120)
		self.Lbl_Proxies_File.configure(activebackground="#f9f9f9")
		self.Lbl_Proxies_File.configure(activeforeground="black")
		self.Lbl_Proxies_File.configure(background="#e6e6e6")
		self.Lbl_Proxies_File.configure(borderwidth="0")
		self.Lbl_Proxies_File.configure(disabledforeground="#a3a3a3")
		self.Lbl_Proxies_File.configure(font="-family {Calibri} -size 10")
		self.Lbl_Proxies_File.configure(foreground="#000000")
		self.Lbl_Proxies_File.configure(highlightbackground="#d9d9d9")
		self.Lbl_Proxies_File.configure(highlightcolor="black")
		self.Lbl_Proxies_File.configure(relief="ridge")
		self.Lbl_Proxies_File.configure(text='None')

		self.Btn_Proxies = tk.Button(self.Frm_UpLeft)
		self.Btn_Proxies.place(relx=0.716, rely=0.4, height=25, width=70)
		self.Btn_Proxies.configure(activebackground="#ececec")
		self.Btn_Proxies.configure(activeforeground="#000000")
		self.Btn_Proxies.configure(anchor='n')
		self.Btn_Proxies.configure(background="#3f3f3f")
		self.Btn_Proxies.configure(disabledforeground="#a3a3a3")
		self.Btn_Proxies.configure(font="-family {Calibri} -size 10 -weight bold -underline 1")
		self.Btn_Proxies.configure(foreground="#ffffff")
		self.Btn_Proxies.configure(highlightbackground="#d9d9d9")
		self.Btn_Proxies.configure(highlightcolor="black")
		self.Btn_Proxies.configure(pady="0")
		self.Btn_Proxies.configure(relief="groove")
		self.Btn_Proxies.configure(text='''Browse''')
		self.Btn_Proxies.configure(command=partial(self.browseFiles, 'proxies'))

		self.Lbl_Tracks = tk.Label(self.Frm_UpLeft)
		self.Lbl_Tracks.place(relx=0.06, rely=0.667, height=29, width=90)
		self.Lbl_Tracks.configure(activebackground="#ffffff")
		self.Lbl_Tracks.configure(activeforeground="black")
		self.Lbl_Tracks.configure(anchor='n')
		self.Lbl_Tracks.configure(background="#3f3f3f")
		self.Lbl_Tracks.configure(disabledforeground="#a3a3a3")
		self.Lbl_Tracks.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Tracks.configure(foreground="#ffffff")
		self.Lbl_Tracks.configure(highlightbackground="#d9d9d9")
		self.Lbl_Tracks.configure(highlightcolor="black")
		self.Lbl_Tracks.configure(relief="ridge")
		self.Lbl_Tracks.configure(text='''Tracks:''')

		self.Lbl_Tracks_File = tk.Label(self.Frm_UpLeft)
		self.Lbl_Tracks_File.place(relx=0.328, rely=0.673, height=25, width=120)
		self.Lbl_Tracks_File.configure(activebackground="#f9f9f9")
		self.Lbl_Tracks_File.configure(activeforeground="black")
		self.Lbl_Tracks_File.configure(background="#e6e6e6")
		self.Lbl_Tracks_File.configure(borderwidth="0")
		self.Lbl_Tracks_File.configure(disabledforeground="#a3a3a3")
		self.Lbl_Tracks_File.configure(font="-family {Calibri} -size 10")
		self.Lbl_Tracks_File.configure(foreground="#000000")
		self.Lbl_Tracks_File.configure(highlightbackground="#d9d9d9")
		self.Lbl_Tracks_File.configure(highlightcolor="black")
		self.Lbl_Tracks_File.configure(relief="ridge")
		self.Lbl_Tracks_File.configure(text='None')

		self.Btn_Tracks = tk.Button(self.Frm_UpLeft)
		self.Btn_Tracks.place(relx=0.716, rely=0.667, height=25, width=70)
		self.Btn_Tracks.configure(activebackground="#ececec")
		self.Btn_Tracks.configure(activeforeground="#000000")
		self.Btn_Tracks.configure(anchor='n')
		self.Btn_Tracks.configure(background="#3f3f3f")
		self.Btn_Tracks.configure(disabledforeground="#a3a3a3")
		self.Btn_Tracks.configure(font="-family {Calibri} -size 10 -weight bold -underline 1")
		self.Btn_Tracks.configure(foreground="#ffffff")
		self.Btn_Tracks.configure(highlightbackground="#d9d9d9")
		self.Btn_Tracks.configure(highlightcolor="black")
		self.Btn_Tracks.configure(pady="0")
		self.Btn_Tracks.configure(relief="groove")
		self.Btn_Tracks.configure(text='''Browse''')
		self.Btn_Tracks.configure(command=partial(self.browseFiles, 'tracks'))

		self.Frm_DownRight = tk.Frame(self.Frm_Main)
		self.Frm_DownRight.place(relx=0.33, rely=0.364, relheight=0.636, relwidth=0.654)

		self.Frm_DownRight.configure(relief='ridge')
		self.Frm_DownRight.configure(borderwidth="2")
		self.Frm_DownRight.configure(relief="ridge")
		self.Frm_DownRight.configure(background="#1b1b1b")

		self.Console_Output = scroll.ScrolledText(self.Frm_DownRight)
		self.Console_Output.place(relx=0.022, rely=0.032, relheight=0.933, relwidth=0.954)
		self.Console_Output.configure(background="#5f5f5f")
		self.Console_Output.configure(borderwidth="2")
		self.Console_Output.configure(font="-family {Calibri} -size 11")
		self.Console_Output.configure(foreground="black")
		self.Console_Output.configure(highlightbackground="#d9d9d9")
		self.Console_Output.configure(highlightcolor="black")
		self.Console_Output.configure(insertbackground="black")
		self.Console_Output.configure(padx="8")
		self.Console_Output.configure(relief="ridge")
		self.Console_Output.configure(selectbackground="black")
		self.Console_Output.configure(selectforeground="white")
		self.Console_Output.configure(wrap="none")

		self.Frm_DownLeft = tk.Frame(self.Frm_Main)
		self.Frm_DownLeft.place(relx=0.029, rely=0.364, relheight=0.636
		        , relwidth=0.28)
		self.Frm_DownLeft.configure(relief='ridge')
		self.Frm_DownLeft.configure(borderwidth="2")
		self.Frm_DownLeft.configure(relief="ridge")
		self.Frm_DownLeft.configure(background="#1b1b1b")
		self.Frm_DownLeft.configure(highlightbackground="#d9d9d9")
		self.Frm_DownLeft.configure(highlightcolor="black")

		self.Lbl_Threads = tk.Label(self.Frm_DownLeft)
		self.Lbl_Threads.place(relx=0.103, rely=0.063, height=29, width=150)
		self.Lbl_Threads.configure(activebackground="#ffffff")
		self.Lbl_Threads.configure(activeforeground="black")
		self.Lbl_Threads.configure(anchor='nw')
		self.Lbl_Threads.configure(background="#3f3f3f")
		self.Lbl_Threads.configure(disabledforeground="#a3a3a3")
		self.Lbl_Threads.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Threads.configure(foreground="#ffffff")
		self.Lbl_Threads.configure(highlightbackground="#d9d9d9")
		self.Lbl_Threads.configure(highlightcolor="black")
		self.Lbl_Threads.configure(padx="5")
		self.Lbl_Threads.configure(relief="ridge")
		self.Lbl_Threads.configure(text='Threads: {}'.format(self.threads))

		self.Lbl_Streams = tk.Label(self.Frm_DownLeft)
		self.Lbl_Streams.place(relx=0.103, rely=0.19, height=29, width=150)
		self.Lbl_Streams.configure(activebackground="#ffffff")
		self.Lbl_Streams.configure(activeforeground="black")
		self.Lbl_Streams.configure(anchor='nw')
		self.Lbl_Streams.configure(background="#3f3f3f")
		self.Lbl_Streams.configure(disabledforeground="#a3a3a3")
		self.Lbl_Streams.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Streams.configure(foreground="#ffffff")
		self.Lbl_Streams.configure(highlightbackground="#d9d9d9")
		self.Lbl_Streams.configure(highlightcolor="black")
		self.Lbl_Streams.configure(padx="5")
		self.Lbl_Streams.configure(relief="ridge")
		self.Lbl_Streams.configure(text='Streams: {}'.format(self.save['streams']))

		self.Lbl_Earnings = tk.Label(self.Frm_DownLeft)
		self.Lbl_Earnings.place(relx=0.103, rely=0.317, height=29, width=150)
		self.Lbl_Earnings.configure(activebackground="#ffffff")
		self.Lbl_Earnings.configure(activeforeground="black")
		self.Lbl_Earnings.configure(anchor='nw')
		self.Lbl_Earnings.configure(background="#3f3f3f")
		self.Lbl_Earnings.configure(disabledforeground="#a3a3a3")
		self.Lbl_Earnings.configure(font="-family {Calibri} -size 12 -weight bold")
		self.Lbl_Earnings.configure(foreground="#ffffff")
		self.Lbl_Earnings.configure(highlightbackground="#d9d9d9")
		self.Lbl_Earnings.configure(highlightcolor="black")
		self.Lbl_Earnings.configure(padx="5")
		self.Lbl_Earnings.configure(relief="ridge")
		self.Lbl_Earnings.configure(text='Earnings: {:.2f}$'.format(self.save['earnings']))

		self.Frm_UpRight = tk.Frame(self.Frm_Main)
		self.Frm_UpRight.place(relx=0.532, rely=0.04, relheight=0.303
		        , relwidth=0.451)
		self.Frm_UpRight.configure(relief='ridge')
		self.Frm_UpRight.configure(borderwidth="3")
		self.Frm_UpRight.configure(relief="ridge")
		self.Frm_UpRight.configure(background="#1b1b1b")
		self.Frm_UpRight.configure(highlightbackground="#d9d9d9")
		self.Frm_UpRight.configure(highlightcolor="black")

		self.Btn_Start = tk.Button(self.Frm_UpRight)
		self.Btn_Start.place(relx=0.096, rely=0.2, height=44, width=107)
		self.Btn_Start.configure(activebackground="#ececec")
		self.Btn_Start.configure(activeforeground="#000000")
		self.Btn_Start.configure(background="#114a0b")
		self.Btn_Start.configure(disabledforeground="#a3a3a3")
		self.Btn_Start.configure(font="-family {Calibri} -size 18 -weight bold")
		self.Btn_Start.configure(foreground="#000000")
		self.Btn_Start.configure(highlightbackground="#d9d9d9")
		self.Btn_Start.configure(highlightcolor="black")
		self.Btn_Start.configure(pady="0")
		self.Btn_Start.configure(relief="groove")
		self.Btn_Start.configure(text='''START''')
		self.Btn_Start.configure(command=self.start_command)

		self.Btn_Stop = tk.Button(self.Frm_UpRight)
		self.Btn_Stop.place(relx=0.548, rely=0.2, height=44, width=107)
		self.Btn_Stop.configure(activebackground="#ececec")
		self.Btn_Stop.configure(activeforeground="#000000")
		self.Btn_Stop.configure(background="#6c0003")
		self.Btn_Stop.configure(disabledforeground="#a3a3a3")
		self.Btn_Stop.configure(font="-family {Calibri} -size 18 -weight bold")
		self.Btn_Stop.configure(foreground="#000000")
		self.Btn_Stop.configure(highlightbackground="#d9d9d9")
		self.Btn_Stop.configure(highlightcolor="black")
		self.Btn_Stop.configure(pady="0")
		self.Btn_Stop.configure(relief="groove")
		self.Btn_Stop.configure(text='''STOP''')
		self.Btn_Stop.configure(command=self.stop_command)

		self.Lbl_Status = tk.Label(self.Frm_UpRight)
		self.Lbl_Status.place(relx=0.318, rely=0.6, height=30, width=114)
		self.Lbl_Status.configure(background="#444444")
		self.Lbl_Status.configure(disabledforeground="#a3a3a3")
		self.Lbl_Status.configure(font="-family {Calibri} -size 13")
		self.Lbl_Status.configure(foreground="#ffffff")
		self.Lbl_Status.configure(text='OFF')

	def refresh(self):
		if self.napsterbot:
			self.threads = self.napsterbot.get_nbthreads()
			if not self.napsterbot.stopped:
				self.napsterbot.check_threads()
				new_logs = self.napsterbot.check_logs()
				for log in new_logs:
					self.Console_Output.insert(tk.END, log)
					self.Console_Output.see("end")
				if float(self.Console_Output.index('end')) > 100:
					self.Console_Output.delete('1.0', '2.0')
				self.streams = self.save['streams'] + self.napsterbot.get_nbstreams()
				self.earnings = self.streams * 0.019
				nm.save({'streams':self.streams, 'earnings':self.earnings}, 'save')
				self.Lbl_Threads.configure(text='Threads: {}'.format(self.threads))
				self.Lbl_Streams.configure(text='Streams: {}'.format(self.streams))
				self.Lbl_Earnings.configure(text='Earnings: {:.2f}$'.format(self.earnings))

        
	def start_command(self):
		self.save = nm.load('save')
		if self.accounts_path and self.proxies_path and self.tracks_path:
			try:
				self.napsterbot = NapsterBot(self.accounts_path, self.proxies_path, self.tracks_path)
			except Exception as e:
				message = 'Could not create a napsterbot instance => {}\n'.format(e)
				self.Console_Output.insert(tk.END, message)
				self.Console_Output.see("end")
				return
			self.Lbl_Status.configure(text='Running...')
			self.bot_thread = threading.Thread(target=self.napsterbot.start)
			self.bot_thread.start()
		else:
			message = 'Files are missing ...\n'
			self.Console_Output.insert(tk.END, message)
			self.Console_Output.see("end")
        
	def stop_command(self):
		nm.save({'streams':self.streams, 'earnings':self.earnings}, 'save')
		self.napsterbot.stop()
		self.bot_thread.join()
		self.Lbl_Status.configure(text='OFF')
        
	def browseFiles(self, file):
		filename = filedialog.askopenfilename(title='Select a file.', filetypes=[("Text files", ".txt")] )
		if filename:
			if file == 'accounts':
				self.Lbl_Accounts_File.configure(text=os.path.basename(filename))
				self.accounts_path = filename
			elif file == 'proxies':
				self.Lbl_Proxies_File.configure(text=os.path.basename(filename))
				self.proxies_path = filename
			elif file == 'tracks':
				self.Lbl_Tracks_File.configure(text=os.path.basename(filename))
				self.tracks_path = filename

	def start(self):
		while True:
			try:
				self.top.update_idletasks()
				self.top.update()
				self.refresh()
			except Exception as e:
				print(type(e),':',e)
				break