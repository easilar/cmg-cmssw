import PhysicsTools.HeppyCore.framework.config as cfg

import os

#####COMPONENT CREATOR

from CMGTools.TTHAnalysis.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
json=dataDir+'/json/Cert_Run2012ABCD_22Jan2013ReReco.json'
### samples for HCAL reco validation

triggers_HT = [
    "HLT_HT200_v*",
    "HLT_HT250_v*",
    "HLT_HT300_v*",
    "HLT_HT350_v*",
    "HLT_HT450_v*",
    "HLT_HT550_v*",
    "HLT_HT650_v*",
    "HLT_HT750_v*",
    ]

#JetHT_HcalExtValid_jet2012D_v1 = cfg.DataComponent(
#    name = 'JetHT_HcalExtValid_jet2012D_v1',
#    files = kreator.getFilesFromEOS('JetHT_HcalExtValid_jet2012D_v1', '/JetHT/CMSSW_7_3_2_patch1-GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v1/MINIAOD', '/store/relval/CMSSW_7_3_2_patch1/JetHT/MINIAOD/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v1/00000/'),
#    intLumi = 1,
#    triggers = [],
#    json = json
#    )
JetHT_HcalExtValid_jet2012D_v2 = cfg.DataComponent(
    name = 'JetHT_HcalExtValid_jet2012D_v2',
    files = kreator.getFilesFromEOS('JetHT_HcalExtValid_jet2012D_v2', '/JetHT/CMSSW_7_3_2_patch1-GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/MINIAOD', '/store/relval/CMSSW_7_3_2_patch1/JetHT/MINIAOD/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/'),
    intLumi = 1,
    triggers = [],
    json = json
    )
DoubleMuparked_HcalExtValid_jet2012D_v1 = cfg.DataComponent(
    name = 'DoubleMuparked_HcalExtValid_jet2012D_v1',
    files = kreator.getFilesFromEOS('DoubleMuparked_HcalExtValid_jet2012D_v1', '/DoubleMuParked/CMSSW_7_3_2_patch1-GR_R_73_V0_HcalExtValid_RelVal_zMu2012D-v1/MINIAOD', '/store/relval/CMSSW_7_3_2_patch1/DoubleMuParked/MINIAOD/GR_R_73_V0_HcalExtValid_RelVal_zMu2012D-v1/00000/'),
    intLumi = 1,
    triggers = [],
    json = json
    )

dataSamplesAll = [ JetHT_HcalExtValid_jet2012D_v2, DoubleMuparked_HcalExtValid_jet2012D_v1]

#-----------DATA---------------

for comp in dataSamplesAll:
    comp.splitFactor = 3
    comp.triggers = []
    comp.triggers = triggers_HT
#    comp.isMC = False
#    comp.isData = True

#if __name__ == "__main__":
#   import sys
#   if "test" in sys.argv:
#       from CMGTools.TTHAnalysis.samples.ComponentCreator import testSamples
#       testSamples(mcSamples)
