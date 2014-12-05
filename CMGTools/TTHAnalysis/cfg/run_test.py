##########################################################
##       CONFIGURATION FOR ME                           ##
##########################################################

#from optparse import OptionParser
#parser = OptionParser()
#parser.add_option("--selectedComponents", dest="allsamples", default="T5Full_1200_1000_800", type="string", action="store", help="samples:Which samples.")
#(options, args) = parser.parse_args()


import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.RootTools.RootTools import *

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import * 

ttHLepAna.loose_muon_pt  = 10
ttHLepAna.loose_muon_relIso = 0.3
ttHLepAna.loose_electron_pt  = 10
ttHLepAna.loose_electron_relIso = 0.2
ttHLepAna.ele_isoCorr = "deltaBeta" 

# Redefine what I need

# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999
#ttHJetMETSkim.metCut = 100
#ttHLepSkim.idCut  = ""
#ttHLepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
ttHJetAna.minLepPt = 10 
ttHJetMCAna.smearJets     = False # do we need to smear the jets?

# Event Analyzer for susy multi-lepton (at the moment, it's the TTH one)
ttHEventAna = cfg.Analyzer(
    'ttHLepEventAnalyzer',
    minJets25 = 0,
    )


ttHIsoTrackAna = cfg.Analyzer(
            'ttHIsoTrackAnalyzer',
            candidates='packedPFCandidates',
            candidatesTypes='std::vector<pat::PackedCandidate>',
            ptMin = 5, # for pion 
            ptMinEMU = 5, # for EMU
            dzMax = 0.1,
            isoDR = 0.3,
            ptPartMin = 0,
            dzPartMax = 0.1,
            maxAbsIso = 8,
            MaxIsoSum = 0.1, ### unused
            MaxIsoSumEMU = 0.2, ### unused
            doSecondVeto = False
            )

from CMGTools.TTHAnalysis.samples.triggers_8TeV_v517 import triggers_1mu, triggers_1muHT, triggers_1eleHT

# Tree Producer
treeProducer = cfg.Analyzer(
    'treeProducerSusySingleLepton',
    vectorTree = True,
    saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
    PDFWeights = PDFWeights,
    triggerBits = {
            'MuHT' : triggers_1muHT,
            'eleHT' : triggers_1eleHT
        }
    )


#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14 import *
#selectedComponents = [ SingleMu, DoubleElectron, TTHToWW_PUS14, DYJetsM50_PU20bx25, TTJets_PUS14 ]

#from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
#selectedComponents = [ T5Full_1200_1000_800 ] 
#selectedComponents = [ T5Full_1500_800_100  ] 

from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14 import SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170, SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170
selectedComponents = [SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170, SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170]

#exec('selectedComponents=['+options.selectedComponents+']')

#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
    ttHIsoTrackAna,
    ttHEventAna,
    treeProducer,
    ])

test = 0
for comp in selectedComponents:
  comp.splitFactor=10
##-------- HOW TO RUN
if test==1:
    # test a single component, using a single thread.
    comp = selectedComponents[0] 
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
elif test==2:    
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:1]
#else:


config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
