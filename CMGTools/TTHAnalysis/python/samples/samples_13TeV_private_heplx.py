import CMGTools.RootTools.fwlite.Config as cfg
import os
from Workspace.HEPHYPythonTools.helpers import getFileList
from Workspace.HEPHYPythonTools.xsec import xsec

def createComponentFromDPM(name, dbsName, dir, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1): 
  component = cfg.MCComponent(
      dataset=dbsName,
      name = name,
      files = getFileList(dir, minAgeDPM=0, histname=histname, xrootPrefix=xrootPrefix, maxN=maxN),
      xSection = xsec[dbsName],
      nGenEvents = 1,
      triggers = [],
      effCorrFactor = 1,
  )
  return component

allComps=[]

T5Full_1200_1000_800 = createComponentFromDPM(\
  name = 'T5Full_1200_1000_800',
  dbsName='/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/schoef-T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER',
  dir='/dpm/oeaw.ac.at/home/cms/store/user/schoef/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD/92bfc1aa0ef8c674e0edabb945b19298', 
  ) 
allComps.append(T5Full_1200_1000_800)

T5Full_1500_800_100 = createComponentFromDPM(\
  name = 'T5Full_1500_800_100',
  dbsName='/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/schoef-T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER',
  dir='/dpm/oeaw.ac.at/home/cms/store/user/schoef/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD/92bfc1aa0ef8c674e0edabb945b19298', 
  ) 
allComps.append(T5Full_1500_800_100)

dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
from CMGTools.TTHAnalysis.setup.Efficiencies import eff2012
for comp in allComps:
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.isMC = True
    comp.isData = False
    comp.efficiency = eff2012

