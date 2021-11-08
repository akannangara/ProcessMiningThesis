import os
import pandas as pd
import JiraConfig as cfg

import pm4py as pm4py

#Dataframe conversions
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

#Process miners
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner

#directly follows graph
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

#visualization
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.footprints import visualizer as fps_visualizer

#petrinets
from pm4py.objects.petri_net.obj import PetriNet, Marking

class ProcessMiner:
    def __init__(self):
        os.environ["PATH"] += os.pathsep + cfg.GraphVizLocation
        self._csvEventLog, self._eventLog = self.readCSVlog()

    def readCSVlog(self, logfile=cfg.DataStoreFolder+"\EventLogCollection.csv"):
        log = pd.read_csv(logfile, sep=',')
        log.rename(columns={'IssueId' : 'case:clientId',
                                'Activity':'concept:name',
                                'Key':'case:concept:name',
                                'TimeStamp':'timestamp'}, inplace=True)
        log = dataframe_utils.convert_timestamp_columns_in_df(log)
        return log, log_converter.apply(log)

    #convert timestamp to time:timestamp
    def eventLogTimeConverter(self, log):
        log.rename(columns={'timestamp' : 'time:timestamp'}, inplace=True)
        return log_converter.apply(log)


    #-----DISCOVERY ALGORITHMS - return the created model + initial/final markings if relevant
    #petrinets
    def PetriNetAlphaMiner(self, eventLog=None, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        net, initial_marking, final_marking = alpha_miner.apply(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['alphaMiner']))
        return net, initial_marking, final_marking

    def PetriNetAlphaPlusMiner(self, eventLog=None, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['alphaPlusMiner']))
        return net, initial_marking, final_marking

    def PetriNetInductiveMiner(self, eventLog=None, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        net, initial_marking, final_marking = inductive_miner.apply(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['initialMiner']))
        return net, initial_marking, final_marking

    def PetriNetHeuristicsMiner(self, eventLog=None, threshold=0.99, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: threshold}
        net, initial_marking, final_marking = heuristics_miner.apply(eventLog, parameters=parameters)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['heuristicsMiner']))
        return net, initial_marking, final_marking

    #heuristicsNet
    def HeuristicsNetMiner(self, eventLog=None, dependency_threshhold=0.5, and_threshold=0.65, loop_2_threshold=0.5, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        heuristics_net = pm4py.discover_heuristics_net(eventLog, dependency_threshhold, and_threshold, loop_2_threshold)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = hn_visualizer.apply(heuristics_net, parameters=parameters)
        hn_visualizer.view(gviz)
        if (save):
            hn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['heuristicsMiner']))
        return heuristics_net

    #directlyFollowsGraph
    def DFG(self, csvEventLog=None, save=False):
        if (csvEventLog==None):
            csvEventLog=self._csvEventLog
        eventLog = self.eventLogTimeConverter(csvEventLog)
        dfg = dfg_discovery.apply(eventLog)
        gviz = dfg_visualization.apply(dfg, log=event_log, variant=dfg_visualization.Variants.FREQUENCY)
        dfg_visualization.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['dfg']))
        return dfg

    #processTree
    def ProcessTreeInductive(self, eventLog=None, noiseThreshold=0.0, save=False):
        if (eventLog==None):
            eventLog=self._eventLog
        processTree = pm4py.discover_process_tree_inductive(eventLog, noise_threshold=noiseThreshold)
        gviz = pt_visualizer.apply(processTree, variant=pt_visualizer.Variants.WO_DECORATION)
        pt_visualizer.view(gviz)
        if (save):
            pt_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['heuristicsMiner']))
        return processTree

    #eventuallyFollowsGraph
    def EFG(self, csvEventLog=None, save=False):
        if (csvEventLog==None):
            csvEventLog=self._csvEventLog
        eventLog = self.eventLogTimeConverter(csvEventLog)
        efg = pm4py.discover_eventually_follows_graph(eventLog)
        print(efg)
        return efg

    def FPS(self, logOrModel=None, save=False):
        if (logOrModel==None):
            logOrModel=self._eventLog
        fps = pm4py.discover_footprints(logOrModel)
#        for fp in range(len(fps)):
#            gviz = fps_visualizer.apply(fps[fp])
#            fps_visualizer.view(gviz)
#        if (save):
#            fps_visualizer.save(gviz, os.path.join(cfg.ImageStorage['base'],cfg.ImageStore['dfg']))
        return fps



    def ExpectedBasisPN(self):
        net = PetriNet("JiraProcess")
        dataframe = pd.read_csv(cfg.JiraExpectedProcess)


if __name__ == "__main__":
    pm = ProcessMiner()
    pm.PetriNetAlphaMiner()
    pm.PetriNetAlphaPlusMiner()
    pm.PetriNetInductiveMiner()
    pm.PetriNetHeuristicsMiner()
    pm.HeuristicsNetMiner()
    pm.ProcessTreeInductive()
    pm.EFG()
    #pm.FPS()