from math import pi, sqrt, cos, sin

import ROOT
ROOT.gStyle.SetOptStat(0)
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

small = False

edmCollections = { \
  "slimmedMETs"                       :("vector<pat::MET>",      "slimmedMETs"                         , "",        "RECO"   )  ,
  "patJets"                           :("vector<pat::Jet>",      "patJets"                             , "",        "RERUN" )  ,
  "patJetsNoHF"                           :("vector<pat::Jet>",      "patJetsNoHF"                             , "",        "RERUN" )  ,
#  "patJetsResDown"                    :("vector<pat::Jet>",      "patJetsResDown"                      , "",        "RERUN" )  ,
#  "patJetsResUp"                      :("vector<pat::Jet>",      "patJetsResUp"                        , "",        "RERUN" )  ,
#  "patSmearedJets"                    :("vector<pat::Jet>",      "patSmearedJets"                      , "",        "RERUN" )  ,
#  "selectedPatJets"                   :("vector<pat::Jet>",      "selectedPatJets"                     , "",        "RERUN" )  ,
#  "selectedPatJetsForMetT1T2Corr"     :("vector<pat::Jet>",      "selectedPatJetsForMetT1T2Corr"       , "",        "RERUN" )  ,
#  "selectedPatJetsForMetT1T2SmearCorr":("vector<pat::Jet>",      "selectedPatJetsForMetT1T2SmearCorr"  , "",        "RERUN" )  ,
#  "selectedPatJetsForMetT2Corr"       :("vector<pat::Jet>",      "selectedPatJetsForMetT2Corr"         , "",        "RERUN" )  ,
#  "selectedPatJetsForMetT2SmearCorr"  :("vector<pat::Jet>",      "selectedPatJetsForMetT2SmearCorr"    , "",        "RERUN" )  ,
#  "shiftedPatJetEnDown"               :("vector<pat::Jet>",      "shiftedPatJetEnDown"                 , "",        "RERUN" )  ,
#  "shiftedPatJetEnUp"                 :("vector<pat::Jet>",      "shiftedPatJetEnUp"                   , "",        "RERUN" )  ,
#  "shiftedPatJetResDown"              :("vector<pat::Jet>",      "shiftedPatJetResDown"                , "",        "RERUN" )  ,
#  "shiftedPatJetResUp"                :("vector<pat::Jet>",      "shiftedPatJetResUp"                  , "",        "RERUN" )  ,
#  "patPFMetT1Txy"                     :("vector<pat::MET>",      "patPFMetT1Txy"                       , "",        "RERUN" )  ,
  "slimmedMETsRERUN"                  :("vector<pat::MET>",      "slimmedMETs"                         , "",        "RERUN" ),
  "slimmedMETsNoHFRERUN"                  :("vector<pat::MET>",      "slimmedMETsNoHF"                         , "",        "RERUN" ),
}

handles={k:Handle(edmCollections[k][0]) for k in edmCollections.keys()}

files = ["/afs/hephy.at/user/r/rschoefbeck/CMS/cmssw/CMSSW_7_4_6_patch1/src/corMETMiniAOD_DATA.root"]
#files = ["/afs/hephy.at/user/r/rschoefbeck/CMS/cmssw/CMSSW_7_4_6_patch1/src/corMETMiniAOD_MC.root"]
#files = ["/afs/hephy.at/user/r/rschoefbeck/CMS/cmssw/CMSSW_7_4_6_patch1/src/corMETMiniAOD_data_noResiduals.root"]
#files = ["/afs/hephy.at/user/r/rschoefbeck/CMS/cmssw/CMSSW_7_4_6_patch1/src/corMETMiniAOD_data_residuals.root"]
#files = ["../../TTHAnalysis/cfg/Test/SingleMu_Run2015B_6/cmsswPreProcessing.root"]
#files = ["/afs/cern.ch/user/s/schoef/eos/cms/store/data/Run2015B/SingleMu/MINIAOD/PromptReco-v1/000/250/987/00000/787E4EA9-A525-E511-9647-02163E011DE5.root"]
#files=['/afs/cern.ch/work/s/schoef/CMS/CMSSW_7_4_7/src/CMGTools/TTHAnalysis/cfg/MetType1_jec_Summer15_50nsV2_DATA_GT_74X_dataRun2_Prompt_v1_residuals_False.root']
#files=['/afs/cern.ch/work/s/schoef/CMS/CMSSW_7_4_7/src/CMGTools/TTHAnalysis/cfg/MetType1_jec_Summer15_50nsV2_DATA_GT_74X_dataRun2_Prompt_v1_residuals_True.root']

events = Events(files)
events.toBegin()
products={}
missingCollections=[]
print "Number of events:",events.size()

nevents = min(1, events.size())

for nev in range(nevents):
  if nev%100==0:print nev,'/',nevents
  events.to(nev)
  eaux=events.eventAuxiliary()
  run=eaux.run()           
  event=eaux.event()
  lumi=eaux.luminosityBlock()
  for k in [ x for x in edmCollections.keys() if x not in missingCollections]:
    try:
      events.getByLabel(edmCollections[k][1:],handles[k])
      products[k]=handles[k].product()
    except:
      products[k]=None
      print "Not found:",k
      missingCollections.append(k)
  levels = ["Uncorrected", "L1FastJet", "L2Relative", "L3Absolute", "L2L3Residual"]
  for i, j in enumerate(products["patJets" ]):
    if i==0: 
      l = j.availableJECLevels()
      print ", ".join([l[k] for k in range(l.size())])
#    print " ".join(["%15s: %15f"%(l, j.pt()*j.jecFactor(l)/j.jecFactor('L1FastJet')*j.jecFactor('Uncorrected')) for l in levels])
    print " ".join(["%15s: %15f"%(l, j.pt()*j.jecFactor(l)) for l in levels])

#  dx,dy=0.,0.
#  print "\n%i:%i:%i"%(run,lumi,event)
#  print "reclustered Jets",
#  for i, j in enumerate(products["selectedPatJets" ]):
##  for i, j in enumerate(products["patSmearedJets" ]):
##    if j.pt()>10:
#      dx -= j.px()*(1-j.jecFactor("L1FastJet"))#-j.jecFactor(0)) #j(L1L2L3-L1)-j(raw)# 1-("L1FastJet")-(0)
#      dy -= j.py()*(1-j.jecFactor("L1FastJet"))#-j.jecFactor(0))
##      dx -= j.px()*(1-j.jecFactor(0))
##      dy -= j.py()*(1-j.jecFactor(0))
#      print "%f"%(j.pt()),
#  print
  
# oldMET = products["slimmedMETs"][0]  
# newMET = products["slimmedMETsRERUN"][0] 
# newMETNoHF = products["slimmedMETsNoHFRERUN"][0] 
# print  
# print "mAOD raw         MET", oldMET.uncorrectedPt()
# print "mAOD type1       MET", oldMET.pt()
# print "RERUN raw        MET", newMET.uncorrectedPt()
# print "RERUN type1      MET", newMET.pt()
# print "RERUN NOHF raw   MET", newMETNoHF.uncorrectedPt()
# print "RERUN NOHF type1 MET", newMETNoHF.pt()
