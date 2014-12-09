##########################################################
##       CONFIGURATION FOR SUSY MULTILEPTON TREES       ##
## skim condition: >= 2 loose leptons, no pt cuts or id ##
##########################################################

import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.RootTools.RootTools import *

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import * 

ttHLepAna.loose_muon_pt  = 5
ttHLepAna.loose_muon_relIso = 0.4
ttHLepAna.mu_isoCorr = "deltaBeta" 
#ttHLepAna.loose_muon_absIso5= 10
ttHLepAna.loose_electron_pt  = 7
ttHLepAna.loose_electron_relIso = 0.4
#ttHLepAna.loose_electron_absIso = 10
ttHLepAna.ele_isoCorr = "rhoArea"

# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999

# --- JET-LEPTON CLEANING ---
ttHJetAna.minLepPt        = 10


# Event Analyzer for susy multi-lepton (at the moment, it's the TTH one) // Do we need had W and Top?
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

susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHSVAnalyzer)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHHeavyFlavourHadronAnalyzer)


from CMGTools.TTHAnalysis.samples.triggers_8TeV_v517 import triggers_1mu, triggers_1muHT, triggers_1eleHT # need to update the trigger MET pr HTMET?

# Tree Producer
treeProducer = cfg.Analyzer(
    'treeProducerSusySingleSoftLepton',
    vectorTree = True,
    saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
    PDFWeights = PDFWeights,
    triggerBits = { }
    #        'MuHT' : triggers_1muHT,
    #        'eleHT' : triggers_1eleHT
     #   }
    )


#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14 import *
#TTJets_PUS14.splitFactor=800
#selectedComponents = [ TTJets_PUS14 , WJetsToLNu_HT100to200_PU_S14_POSTLS170, WJetsToLNu_HT200to400_PU_S14_POSTLS170, WJetsToLNu_HT400to600_PU_S14_POSTLS170, WJetsToLNu_HT600toInf_PU_S14_POSTLS170]

from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14 import *
SMS_T1qqqq_2J_mGl1000_mLSP800_PU_S14_POSTLS170.splitFactor=500
#
selectedComponents = [
##  official samples
  SMS_T1qqqq_2J_mGl1000_mLSP800_PU_S14_POSTLS170,
#  SMS_T1qqqq_2J_mGl1400_mLSP100_PU_S14_POSTLS170,
#  SMS_T1bbbb_2J_mGl1000_mLSP900_PU_S14_POSTLS170,
#  SMS_T1bbbb_2J_mGl1500_mLSP100_PU_S14_POSTLS170,
#  SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170,
#  SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170,
#  SMS_T2tt_2J_mStop425_mLSP325_PU_S14_POSTLS170,
#  SMS_T2tt_2J_mStop500_mLSP325_PU_S14_POSTLS170,
#  SMS_T2tt_2J_mStop650_mLSP325_PU_S14_POSTLS170,
#  SMS_T2tt_2J_mStop850_mLSP100_PU_S14_POSTLS170,
#  SMS_T2bb_2J_mStop600_mLSP580_PU_S14_POSTLS170,
#  SMS_T2bb_2J_mStop900_mLSP100_PU_S14_POSTLS170,
#  SMS_T2qq_2J_mStop600_mLSP550_PU_S14_POSTLS170,
#  SMS_T2qq_2J_mStop1200_mLSP100_PU_S14_POSTLS170,
##private samples from GP and MD etc.
#  T5WW_2J_mGo1200_mCh1000_mChi800,
#  T5WW_2J_mGo1500_mCh800_mChi100,
#  T5WW_2J_mGo1400_mCh315_mChi300,
#  T1tttt_2J_mGo1300_mStop300_mCh285_mChi280,
#  T1tttt_2J_mGo1300_mStop300_mChi280,
#  T1tttt_2J_mGo800_mStop300_mCh285_mChi280,
#  T1tttt_2J_mGo800_mStop300_mChi280,
#  T6ttWW_2J_mSbot600_mCh425_mChi50,
#  T6ttWW_2J_mSbot650_mCh150_mChi50,
#  T1ttbb_2J_mGo1500_mChi100
]
#from CMGTools.TTHAnalysis.samples.samples_13TeV_private_lxplus import *
#selectedComponents=[
#  T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec,
#  T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec,
#  T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec,
#  T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec,
#  T1tttt_gluino_1300_LSP_100,
#  T1tttt_gluino_800_LSP_450,
#  T5qqqqWW_Gl_1400_LSP_100_Chi_325,
#  T5qqqqWW_Gl_1400_LSP_300_Chi_315,
#  SqGltttt_Gl_1300_Sq_1300_LSP_100, 
#  T6qqWW_Sq_950_LSP_300_Chi_350
#]

TTJets_PUS14.splitFactor=800
selectedComponents = [ TTJets_PUS14 , WJetsToLNu_HT100to200_PU_S14_POSTLS170, WJetsToLNu_HT200to400_PU_S14_POSTLS170, WJetsToLNu_HT400to600_PU_S14_POSTLS170, WJetsToLNu_HT600toInf_PU_S14_POSTLS170]
selectedComponents += [SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170, SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170]

#from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
#T5Full_1200_1000_800.splitFactor=5
#T5Full_1500_800_100.splitFactor=5
#selectedComponents = [ T5Full_1200_1000_800 , T5Full_1500_800_100] 

#from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14 import SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170, SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170
#selectedComponents = [SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170, SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170]


#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
    ttHIsoTrackAna,
    ttHEventAna,
    treeProducer,
    ])


#-------- HOW TO RUN
test = 0
if test==1:
    # test a single component, using a single thread.
    comp= selectedComponents[0]
    #comp.files = ['root://eoscms//eos/cms/store/cmst3/group/susy/alobanov/MC/MiniAOD/13TeV_Gl_Gl_4q_Gl1400_LSP300_Chi315_MiniAOD.root']
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
elif test==2:    
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = len(comp.files)


config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
