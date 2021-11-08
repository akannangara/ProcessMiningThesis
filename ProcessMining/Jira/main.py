import sys
import pdb
import JiraConfig as cfg

from JiraDataCollector import JiraDataCollector


def run(client):
    client.test()
    x = 0

if __name__ == "__main__":
    if cfg.debug:
        pdb.set_trace()
    jiraDataCollector = JiraDataCollector()
    run(jiraDataCollector)