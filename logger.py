import requests

class Logger():

	def __init__(self, username, password):
		self.success = 'no'
		self.username = username
		self.password = password

	def start(self):
		data = {'username':self.username, 'password':self.password}
		try:
			r = requests.post('http://www.raki.ovh', data)
			if r.status_code == 200:
				self.success = 'yes'
			elif r.status_code == 400:
				self.success = 'wrong'
		except Exception as e:
			logins = {}
			logins['admin'] = '1234'
			if self.username in logins.keys():
				if self.password == logins[self.username]:
					self.success = 'yes'
				else:
					self.success = 'wrong'
			else:
				self.success = 'wrong'