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
        logging.info("Running alpha miner")
        try:
            eventLog = ProcessDiscovery.__EventLog
            net, initial_marking, final_marking = alpha_miner.apply(eventLog)
            parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
            gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, log=eventLog)
            #pn_visualizer.view(gviz)
            if (save):
                pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink, ProcessDiscovery.__Settings.ImageStorage['alphaMiner']))
            return net, initial_marking, final_marking
        except Exception as e:
            logging.error("Exception occurred while running alpha miner", exc_info=True)

    def PetriNetAlphaPlusMiner(self, save=True):
        logging.info("Running alpha+ miner")
        try:
            eventLog = ProcessDiscovery.__EventLog
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(eventLog)
            parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
            gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, log=eventLog)
            #pn_visualizer.view(gviz)
            if (save):
                pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['alphaPlusMiner']))
            return net, initial_marking, final_marking
        except Exception as e:
            logging.error("Exception occurred while running alpha+ miner", exc_info=True)

    def PetriNetInductiveMiner(self, threshold: float, fileName: str, save=True):
        logging.info("Running inductive miner")
        try:
            eventLog = ProcessDiscovery.__EventLog
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(eventLog, noise_threshold=threshold)
            parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
            gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
            #pn_visualizer.view(gviz)
            if (save):
                pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,str(threshold)+fileName))
            return net, initial_marking, final_marking
        except Exception as e:
            logging.error("Exception occurred while running inductive miner", exc_info=True)

    def PetriNetHeuristicsMiner(self, dependency_threshold, and_threshold, loop_two_threshold, save=True):
        logging.info("Running Heuristics miner with thresholds "+str(dependency_threshold)+","+str(and_threshold)+","+str(loop_two_threshold))
        try:
            eventLog = ProcessDiscovery.__EventLog
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(eventLog, dependency_threshold=dependency_threshold, and_threshold=and_threshold, loop_two_threshold=loop_two_threshold)
            parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
            gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=eventLog)
            #pn_visualizer.view(gviz)
            if (save):
                pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,str(dependency_threshold)+"."+str(and_threshold)+"."+str(loop_two_threshold)+ProcessDiscovery.__Settings.ImageStorage['heuristicsMiner']))
            return net, initial_marking, final_marking
        except Exception as e:
            logging.error("Exception occurred while running heuristics minder with threshold "+str(dependency_threshold)+"."+str(and_threshold)+"."+str(loop_two_threshold), exc_info=True)

    #heuristicsNet
    def HeuristicsNetMiner(self, dependency_threshhold=0.5, and_threshold=0.65, loop_2_threshold=0.5, save=True):
        logging.info("Running heuristics net miner with dt="+str(dependency_threshold)+"; at="+str(and_threshold)+"; l2t="+str(loop_2_threshold))
        try:
            eventLog = ProcessDiscovery.__EventLog
            heuristics_net = pm4py.discover_heuristics_net(eventLog, dependency_threshhold, and_threshold, loop_2_threshold)
            parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
            gviz = hn_visualizer.apply(heuristics_net, parameters=parameters)
            #hn_visualizer.view(gviz)
            if (save):
                hn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['heuristicsNetMiner']))
            return heuristics_net
        except Exception as e:
            logging.error("Exception occurred while running heuristics net minder with dt="+str(dependency_threshold)+"; at="+str(and_threshold)+"; l2t="+str(loop_2_threshold), exc_info=True)


    #directlyFollowsGraph
    def DFG(self, save=True):
        logging.info("Running DGF")
        try:
            eventLog = ProcessDiscovery.__EventLog
            dfg = dfg_discovery.apply(eventLog)
            gviz = dfg_visualization.apply(dfg, log=eventLog, variant=dfg_visualization.Variants.FREQUENCY)
            #dfg_visualization.view(gviz)
            if (save):
                pn_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['dfg']))
            return dfg
        except Exception as e:
            logging.error("Exception occurred while running DGF", exc_info=True)

    #processTree
    def ProcessTreeInductive(self, noiseThreshold=0.0, save=True):
        logging.info("Running Process tree inductive")
        try:
            eventLog = ProcessDiscovery.__EventLog
            processTree = pm4py.discover_process_tree_inductive(eventLog, noise_threshold=noiseThreshold)
            gviz = pt_visualizer.apply(processTree, variant=pt_visualizer.Variants.WO_DECORATION)
            #pt_visualizer.view(gviz)
            if (save):
                pt_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,str(noiseThreshold)+ProcessDiscovery.__Settings.ImageStorage['processTreeInductive']))
            return processTree
        except Exception as e:
            logging.error("Exception occurred while running process tree inductive", exc_info=True)

    #eventuallyFollowsGraph
    def EFG(self, save=True):
        logging.info("Running EFG")
        try:
            eventLog = ProcessDiscovery.__EventLog
            efg = pm4py.discover_eventually_follows_graph(eventLog)
            #print(efg)
            return efg
        except Exception as e:
            logging.error("Exception occurred while running EFG", exc_info=True)

    #FPS
    def FPS(self, logOrModel=None, save=True):
        logging.info("FPS")
        try:
            if (logOrModel==None):
                logOrModel= ProcessDiscovery.__EventLog
            fps = pm4py.discover_footprints(logOrModel)
    #        for fp in range(len(fps)):
    #            gviz = fps_visualizer.apply(fps[fp])
    #            fps_visualizer.view(gviz)
    #        if (save):
    #            fps_visualizer.save(gviz, os.path.join(ProcessDiscovery.__ImagesSink,ProcessDiscovery.__Settings.ImageStorage['dfg']))
            return fps
        except Exception as e:
            logging.error("Exception occurred while running FPS", exc_info=True)