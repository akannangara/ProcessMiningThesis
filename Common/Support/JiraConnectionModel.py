class JiraConnectionModel:
		def __init__(self, servername, username, password, timer):
				self.Servername = servername
				self.Username = username
				self.Password = password
				self.ConnectionRefreshTimer = timer