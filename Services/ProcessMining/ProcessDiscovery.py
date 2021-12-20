import logging
import os
import pandas as pd
from pydantic import BaseModel

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

class ProcessDiscovery(BaseModel):
    __Settings = None
    __EventLog = None
    __ImagesSink = None

    def __init__(self, settings, eventLog, onlyDone=False):
        ProcessDiscovery.__Settings = settings
        repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
        ProcessDiscovery.__ImagesSink = os.path.join(repsoitoryLocation, settings.ImageStorage["ImagesSinkProcessDiscovery"])
        if onlyDone:
             ProcessDiscovery.__ImagesSink = os.path.join(ProcessDiscovery.__ImagesSink, "OnlyDone")
        ProcessDiscovery.__EventLog = eventLog

    #-----DISCOVERY ALGORITHMS - return the created model + initial/final markings if relevant
    #petrinets
    def PetriNetAlphaMiner(self, save=True):
        eventLog = ProcessDiscovery.__EventLog
        net, initial_marking, final_marking = alpha_miner.apply(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        #pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink, ProcessDiscovery.__Settings.ImageStorage['alphaMiner']))
        return net, initial_marking, final_marking

    def PetriNetAlphaPlusMiner(self, save=True):
        eventLog = ProcessDiscovery.__EventLog
        net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        #pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['alphaPlusMiner']))
        return net, initial_marking, final_marking

    def PetriNetInductiveMiner(self, save=True):
        eventLog = ProcessDiscovery.__EventLog
        net, initial_marking, final_marking = inductive_miner.apply(eventLog)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        #pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['inductiveMiner']))
        return net, initial_marking, final_marking

    def PetriNetHeuristicsMiner(self, threshold=0.99, save=True):
        eventLog = ProcessDiscovery.__EventLog
        parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: threshold}
        net, initial_marking, final_marking = heuristics_miner.apply(eventLog, parameters=parameters)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
        #pn_visualizer.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,str(threshold)+ProcessDiscovery.__Settings.ImageStorage['heuristicsMiner']))
        return net, initial_marking, final_marking

    #heuristicsNet
    def HeuristicsNetMiner(self, dependency_threshhold=0.5, and_threshold=0.65, loop_2_threshold=0.5, save=True):
        eventLog = ProcessDiscovery.__EventLog
        heuristics_net = pm4py.discover_heuristics_net(eventLog, dependency_threshhold, and_threshold, loop_2_threshold)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = hn_visualizer.apply(heuristics_net, parameters=parameters)
        #hn_visualizer.view(gviz)
        if (save):
            hn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['heuristicsMiner']))
        return heuristics_net

    #directlyFollowsGraph
    def DFG(self, save=True):
        eventLog = ProcessDiscovery.__EventLog
        dfg = dfg_discovery.apply(eventLog)
        gviz = dfg_visualization.apply(dfg, log=eventLog, variant=dfg_visualization.Variants.FREQUENCY)
        #dfg_visualization.view(gviz)
        if (save):
            pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['dfg']))
        return dfg

    #processTree
    def ProcessTreeInductive(self, noiseThreshold=0.0, save=True):
        eventLog = ProcessDiscovery.__EventLog
        processTree = pm4py.discover_process_tree_inductive(eventLog, noise_threshold=noiseThreshold)
        gviz = pt_visualizer.apply(processTree, variant=pt_visualizer.Variants.WO_DECORATION)
        #pt_visualizer.view(gviz)
        if (save):
            pt_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,str(noiseThreshold)+ProcessDiscovery.__Settings.ImageStorage['processTreeInductive']))
        return processTree

    #eventuallyFollowsGraph
    def EFG(self, save=True):
        eventLog = ProcessDiscovery.__EventLog
        efg = pm4py.discover_eventually_follows_graph(eventLog)
        #print(efg)
        return efg

    #FPS
    def FPS(self, logOrModel=None, save=True):
        if (logOrModel==None):
            logOrModel= ProcessDiscovery.__EventLog
        fps = pm4py.discover_footprints(logOrModel)
#        for fp in range(len(fps)):
#            gviz = fps_visualizer.apply(fps[fp])
#            fps_visualizer.view(gviz)
#        if (save):
#            fps_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['dfg']))
        return fps