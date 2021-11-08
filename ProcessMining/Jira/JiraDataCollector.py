import os
import time
import logging
import JiraConfig as cfg
import pandas as pd
from jira import JIRA

from Models.IssueItem import IssueItem
from Models.WorkLogItem import WorkLogItem
from Models.EventLogItem import EventLogItem
from Models.JiraTypes import JiraTypes


class JiraDataCollector:
    typesCollector = JiraTypes()
    issueCollector = {} #{id, issue}
    EventLogCollector = []
    WorkLogCollector = []
    StoragePath = cfg.DataStoreFolder
    JiraConnectTime = time.time() - 60*10


    def __init__(self):
        logging.basicConfig(filename='log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.connectJira()
        self.debug = cfg.debug


    def StoreAllProjects(self, saveStore=False):
        for p in self.collectProjects():
            sTime = time.time()
            logging.info("Start import " + str(p.key) +"...")
            if self.debug:
                print("Start import " + str(p.key) +"...")
            self.StoreProjectIssues(p.key)
            if self.debug:
                print("finished storing project " + str(p.key)+ " after %s s" % (time.time()-sTime))
            logging.info("finished storing project " + str(p.key)+ " after %s s" % (time.time()-sTime))
        if saveStore:
            self.StoreAllLists()


    def StoreProjectIssues(self, project, saveStore=False):
        for issue in self.collectProjectIssues(project):
            self.StoreIssueComplete(self.collectIssue(issue.key))
        if saveStore:
            self.StoreAllLists()


    def StoreIssueComplete(self, issue, saveStore=False):
        self.connectJira()
        self.StoreIssue(issue)
        self.StoreIssueEventLog(issue)
        self.StoreIssueWorkLog(issue)
        logging.info("Stored issue " + issue.key)
        if self.debug:
            print("Stored issue " + issue.key)
        if saveStore:
            self.StoreAllLists()


    def StoreAllLists(self):
        self.StoreItemDictionary(self.issueCollector, "IssueCollection.csv")
        logging.info("Finished storing issue collector")
        self.StoreItemsList(self.EventLogCollector, "EventLogCollection.csv")
        logging.info("Finished storing event log collector")
        self.StoreItemsList(self.WorkLogCollector, "WorkLogCollection.csv")
        logging.info("Finished storing work log collector")
        self.StoreItemDictionary(self.typesCollector.TeamMembers, "TeamMembers.csv")
        logging.info("Finished storing team members collector")
        self.StoreSimpleList(self.typesCollector.PriorityTypes.values(), "PriorityTypes.csv")
        logging.info("Finished storing priority type collector")
        self.StoreSimpleList(self.typesCollector.StatusTypes.values(), "StatusTypes.csv")
        logging.info("Finished storing status type collector")
        self.StoreSimpleList(self.typesCollector.IssueTypes.values(), "IssueTypes.csv")
        logging.info("Finished storing issue type collector")
        self.StoreSimpleList(self.typesCollector.ActivityTypes, "ActivityTypes.csv")
        logging.info("Finished storing activity type collector")


    def StoreSimpleList(self, list, filename):
        with open(os.path.join(self.StoragePath,filename), 'w') as f:
            for i in list:
                f.write(str(i) + '\n')


    def StoreItemDictionary(self, dictionary, filename):
        l = []
        for key, value in dictionary.items():
            l.append(value)
        self.StoreItemsList(l, filename)


    def StoreItemsList(self, list, filename):
        dataframe = pd.DataFrame()
        for i in list:
            properties = i.__dict__
            data = {}
            for key, value in properties.items():
                data[key] = [value]
            dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)
        if filename == "":
            input("please enter file name to store: ")
        dataframe.index.name = "df_index"
        dataframe.to_csv(os.path.join(self.StoragePath,filename))


    def StoreIssueWorkLog(self, issue):
        id = issue.id
        key = issue.key
        if 'worklog' in issue.raw['fields']:
            for worklog in issue.raw['fields']['worklog']['worklogs']:
                w = WorkLogItem()
                w.IssueId = id
                w.Key = key
                w.Authorkey = self.typesCollector.TeamMemberCheck(worklog['author'])
                w.TimeCreated = worklog['created']
                w.TimeSpent = worklog['timeSpentSeconds']
                self.WorkLogCollector.append(w)


    def StoreIssueEventLog(self, issue):
        id = issue.id
        key = issue.key
        initialEvent = EventLogItem()
        initialEvent.IssueId = id
        initialEvent.Key = key
        initialEvent.TeamMemberKey = self.typesCollector.TeamMemberCheck(issue.raw['fields']['creator'])
        initialEvent.TimeStamp = issue.raw['fields']['created']
        initialEvent.From = "INITIAL_NODE"
        initialEvent.Activity = self.typesCollector.ActivityTypesCheck("To Do") #To Do or Backlog?
        self.EventLogCollector.append(initialEvent)
        histories = issue.raw['changelog']['histories']
        for h in histories:
            for i in h['items']:
                if i['field'] in JiraTypes.AcceptedActivities:
                    e = EventLogItem()
                    e.IssueId = id
                    e.Key = key
                    e.TeamMemberKey = self.typesCollector.TeamMemberCheck(h['author'])
                    e.TimeStamp = h['created']
                    e.From = i['fromString']
                    e.Activity = self.typesCollector.ActivityTypesCheck(i['toString'])
                    self.EventLogCollector.append(e)


    def OriginalTimeEstimateCreator(self, issue):
        histories = issue.raw['changelog']['histories']
        for h in histories:
            for i in h['items']:
                if i['field'] == 'timeoriginalestimate':
                    return self.typesCollector.TeamMemberCheck(h['author'])
        return ""


    def StoreIssue(self, issue):
        i = IssueItem()
        issueData = issue.raw['fields']
        i.Key = issue.raw['key']
        i.Id = issue.raw['id']
        _, i.Type = self.typesCollector.IssueTypesCheck(issueData['issuetype']['id'],
                                                issueData['issuetype']['name'])
        i.TimeCreated = issueData['created']
        i.TimeResolved = issueData['resolutiondate']
        if not issueData['priority'] == None:
            _, i.Priority = self.typesCollector.PriorityTypesCheck(issueData['priority']['id'],
                    issueData['priority']['name'])
        else:
            self.typesCollector.PriorityTypesCheck(0, "None")
        i.CreatorKey = self.typesCollector.TeamMemberCheck(issueData['creator'])
        i.DueDate = issueData['duedate']
        if 'timetracking' in issueData:
            if 'originalEstimateSeconds' in issueData['timetracking']:
                i.TimeEstimate = issueData['timetracking']['originalEstimateSeconds']
                i.TimeEstimateCreator = self.OriginalTimeEstimateCreator(issue)
            if 'timeSpentSeconds' in issueData['timetracking']:
                i.TimeSpent = issueData['timetracking']['timeSpentSeconds']
        _, i.Status = self.typesCollector.StatusTypesCheck(issueData['status']['id'],
                                                        issueData['status']['name'])
        i.WorkRatio = issueData['workratio']
        if not i.TimeResolved == None:
            self.issueCollector[i.Key] = i


    def connectJira(self):
        if (time.time() - self.JiraConnectTime) > 60*5:
            servername = cfg.Jira['ServerName']
            username = cfg.Jira['Username']
            password = cfg.Jira['Password']
            self.client = JIRA(servername, basic_auth=(username, password))

    def collectIssue(self, issue):
        return self.client.issue(issue, expand='changelog')

    def collectProjectIssues(self, project):
        return self.client.search_issues(jql_str='project='+project, maxResults=False, expand='changelog')

    def collectProjects(self, **kwargs):
        if 'projectId' in kwargs:
            if type(kwargs['projectId']) == list:
                projects = []
                for pId in kwargs['projectId']:
                    projects.append(self.collectProjects(pId))
                return projects
            return self.client.project(kwargs['projectId'], expand='issue')
        else:
            return self.client.projects()

        

if __name__ == "__main__":
    jiraDataCollector = JiraDataCollector()
    x = jiraDataCollector.collectProjects()
    y = jiraDataCollector.collectIssue('CONBR-121')
    jiraDataCollector.StoreProjectIssues('CONBR', saveStore=True)
    jiraDataCollector.StoreProjectIssues('PSH', saveStore=True)
    jiraDataCollector.StoreAllLists()
    #jiraDataCollector.StoreAllProjects(saveStore=True)