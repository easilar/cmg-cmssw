import CMGTools.RootTools.fwlite.Config as cfg
import os

from CMGTools.TTHAnalysis.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
T5Full_1200_1000_800 = kreator.makeMyPrivateMCComponent("T5Full-1200-1000-800", "/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/schoef-T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER", "PRIVATE", ".*root", "phys03", fileprefix = 'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms')
T5Full_1500_800_100  = kreator.makeMyPrivateMCComponent("T5Full-1500-800-100", "/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/schoef-T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER", "PRIVATE", ".*root", "phys03", fileprefix='root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms')
allComps=[T5Full_1200_1000_800, T5Full_1500_800_100]

dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
from CMGTools.TTHAnalysis.setup.Efficiencies import eff2012
for comp in allComps:
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.isMC = True
    comp.isData = False
    comp.efficiency = eff2012

