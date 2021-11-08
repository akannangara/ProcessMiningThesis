from Models.TeamMember import TeamMember

class JiraTypes:
		PriorityTypes = {} #{id:name}
		StatusTypes = {} #{id:name}
		IssueTypes = {} #{id:name}
		TeamMembers = {} #{key: TeamMember}
		ActivityTypes = []

		AcceptedActivities = ['status']

		def PriorityTypesCheck(self, id, name):
				if not id in self.PriorityTypes:
						self.PriorityTypes[id] = name
				return id, name

		def StatusTypesCheck(self, id, name):
				if not id in self.StatusTypes:
						self.StatusTypes[id] = name
				return id, name

		def IssueTypesCheck(self, id, name):
				if not id in self.IssueTypes:
						self.IssueTypes[id] = name
				return id, name

		def ActivityTypesCheck(self, name):
				if not name in self.ActivityTypes:
						self.ActivityTypes.append(name)
				return name

		def TeamMemberCheck(self, member):
				if not member['key'] in self.TeamMembers:
						m = TeamMember()
						m.Key = member['key']
						m.Name = member['name']
						m.DisplayName = member['displayName']
						m.Active = member['active']
						self.TeamMembers[member['key']] = m
				return member['key']