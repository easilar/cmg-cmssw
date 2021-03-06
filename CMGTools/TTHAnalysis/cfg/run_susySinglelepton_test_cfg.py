##########################################################
##       CONFIGURATION FOR SUSY SINGLELEPTON TREES      ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import * 


#-------- REDEFINE WHAT I NEED -----------

# Lepton Skimming
ttHLepSkim.minLeptons = 1
ttHLepSkim.maxLeptons = 999
#ttHLepSkim.idCut  = ""
#ttHLepSkim.ptCuts = []

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    
# Lepton Preselection
lepAna.loose_electron_id = "POG_MVA_ID_Run2_NonTrig_VLoose"

isolation = "miniIso"
#isolation = "ptRel"
if isolation == "ptRel": 
    # delay isolation cut for leptons of pt > 10, for which we do pTrel recovery
    lepAna.loose_muon_isoCut     = lambda muon : muon.relIso03 < 0.5 or muon.pt() > 10
    lepAna.loose_electron_isoCut = lambda elec : elec.relIso03 < 0.5 or elec.pt() > 10
    # in the cleaning, keep the jet if the lepton fails relIso or ptRel
    jetAna.jetLepArbitration = lambda jet,lepton : (
        lepton if (lepton.relIso03 < 0.4 or ptRelv1(lepton.p4(),jet.p4()) > 5) else jet
    )
    ttHCoreEventAna.leptonMVAKindTTH = "SusyWithBoost"
    ttHCoreEventAna.leptonMVAKindSusy = "SusyWithBoost" 
    ttHCoreEventAna.leptonMVAPathTTH = "CMGTools/TTHAnalysis/macros/leptons/trainingPHYS14leptonMVA_PHYS14eleMVA_MiniIso_ttH/weights/%s_BDTG.weights.xml"
    ttHCoreEventAna.leptonMVAPathSusy = "CMGTools/TTHAnalysis/macros/leptons/trainingPHYS14leptonMVA_PHYS14eleMVA_MiniIso_SusyT1/weights/%s_BDTG.weights.xml"
    # insert a second skimmer after the jet cleaning 
    ttHLepSkim2 = cfg.Analyzer(
        ttHLepSkimmer, name='ttHLepSkimmer2',
        minLeptons = 2,
        maxLeptons = 999,
        )
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, ttHLepSkim2)
elif isolation == "miniIso": 
    lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
    lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == None:
    lepAna.loose_muon_isoCut     = lambda muon : True
    lepAna.loose_electron_isoCut = lambda elec : True
else:
    # nothing to do, will use normal relIso03
    pass

# Switch off slow photon MC matching
photonAna.do_mc_match = False

#Store all gen taus
genAna.allGenTaus = True
genAna.verbose = False
##use latest JEC
#jetAna.recalibrationType="AK4PFchs"
#jetAna.mcGT="Summer15_V4_MC"

#-------- ADDITIONAL ANALYZERS -----------

## Event Analyzer for susy single-lepton (at the moment, it's the TTH one)
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## JetTau analyzer, to be called (for the moment) once bjetsMedium are produced
from CMGTools.TTHAnalysis.analyzers.ttHJetTauAnalyzer import ttHJetTauAnalyzer
ttHJetTauAna = cfg.Analyzer(
    ttHJetTauAnalyzer, name="ttHJetTauAnalyzer",
    )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHSVAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHHeavyFlavourHadronAna)

### Insert declustering analyzer
#from CMGTools.TTHAnalysis.analyzers.ttHDeclusterJetsAnalyzer import ttHDeclusterJetsAnalyzer
#ttHDecluster = cfg.Analyzer(
#    ttHDeclusterJetsAnalyzer, name='ttHDecluster',
#    lepCut     = lambda lep,ptrel : lep.pt() > 10,
#    maxSubjets = 6, # for exclusive reclustering
#    ptMinSubjets = 5, # for inclusive reclustering
#    drMin      = 0.2, # minimal deltaR(l,subjet) required for a successful subjet match
#    ptRatioMax = 1.5, # maximum pt(l)/pt(subjet) required for a successful match
#    ptRatioDiff = 0.1,  # cut on abs( pt(l)/pt(subjet) - 1 ) sufficient to call a match successful
#    drMatch     = 0.02, # deltaR(l,subjet) sufficient to call a match successful
#    ptRelMin    = 5,    # maximum ptRelV1(l,subjet) sufficient to call a match successful
#    prune       = True, # also do pruning of the jets 
#    pruneZCut       = 0.1, # pruning parameters (usual value in CMS: 0.1)
#    pruneRCutFactor = 0.5, # pruning parameters (usual value in CMS: 0.5)
#    verbose     = 0,   # print out the first N leptons
#    jetCut = lambda jet : jet.pt() > 20,
#    mcPartonPtCut = 20,
#    mcLeptonPtCut =  5,
#    mcTauPtCut    = 15,
#    )
#susyCoreSequence.insert(susyCoreSequence.index(ttHFatJetAna)+1, ttHDecluster)


from CMGTools.TTHAnalysis.analyzers.treeProducerSusySingleLepton import * 
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusySingleLepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susySingleLepton_globalVariables,
     globalObjects = susySingleLepton_globalObjects,
     collections = susySingleLepton_collections,
)

## histo counter
susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
                        susyCounter)


#-------- SAMPLES AND TRIGGERS -----------


from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import triggers_mumu_iso, triggers_mumu_noniso, triggers_ee, triggers_3e, triggers_mue, triggers_1mu_iso, triggers_1e
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuNoIso' : triggers_mumu_noniso,
    'DoubleEl' : triggers_ee,
    'TripleEl' : triggers_3e,
    'MuEG'     : triggers_mue,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl' : triggers_1e,
}

from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
from CMGTools.TTHAnalysis.samples.samples_13TeV_CSA14v2 import SingleMu

selectedComponents = [
  ] + WJetsToLNuHT + DYJetsM50HT + [ #DYJetsToLL_M50,
   TTJets ]+ SingleTop +[
   TTWJets,TTZJets, TTH,
   WZJetsTo3LNu, ZZTo4L,
   #GGHZZ4L, GGHTT, VBFTT, 
   SMS_T1tttt_2J_mGl1500_mLSP100, SMS_T1tttt_2J_mGl1200_mLSP800,
   T5ttttDeg_mGo1000_mStop300_mCh285_mChi280, T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_dil,
   T5qqqqWW_mGo1200_mCh1000_mChi800_dilep, T5qqqqWWDeg_mGo1000_mCh315_mChi300_dilep
]
if False:
    ttHLepSkim.minLeptons = 1
    QCDPtEMEnriched.remove(QCD_Pt10to20_EMEnriched)
    selectedComponents = [ QCD_Mu15 ] + QCD_Mu5 + QCDPtEMEnriched + QCDPtbcToE


# -- fine splitting, for some private MC samples with a single file
#for comp in selectedComponents:
#    comp.splitFactor = 1
#    comp.fineSplitFactor = 40

    
#-------- SEQUENCE -----------

sequence = cfg.Sequence(susyCoreSequence+[
        ttHJetTauAna,
        ttHEventAna,
        treeProducer,
    ])


#-------- HOW TO RUN -----------

from PhysicsTools.HeppyCore.framework.heppy import getHeppyOption
test = getHeppyOption('test')
print "Running with option %s"%test
if test == '1':
    comp = TTH
    if getHeppyOption('T1tttt'):
        comp = SMS_T1tttt_2J_mGl1500_mLSP100
    if getHeppyOption('H4L'):
        comp = GGHZZ4L
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    if not getHeppyOption('single'):
        comp.fineSplitFactor = 4
    selectedComponents = [ comp ]
elif test == '2':
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
elif test == 'EOS':
    comp = DYJetsToLL_M50#TTJets
    comp.files = comp.files[:1]
    if getHeppyOption('Wigner'):
        print "Will read from WIGNER"
        comp.files = [ 'root://eoscms//eos/cms/store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/0432E62A-7A6C-E411-87BB-002590DB92A8.root' ]
    else:
        print "Will read from CERN Meyrin"
        comp.files = [ 'root://eoscms//eos/cms/store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/10000/F675C068-5E6C-E411-B915-0025907DC9AC.root' ]
    os.system("/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select fileinfo "+comp.files[0].replace("root://eoscms//","/"))
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test == 'SingleMu':
    comp = SingleMu
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    selectedComponents = [ comp ]
elif test == '74X-MC':
    from CMGTools.TTHAnalysis.samples.samples_13TeV_74X import *
    what = getHeppyOption("sample")
    if what == "TT":
        ttHLepSkim.minLeptons = 0
        selectedComponents = [ TTJets ]
    elif what == "Z":
        selectedComponents = [ ZEE_bx25, ZMM_bx25, ZTT_bx25 ]
    elif what == "TTJets_LO":
        selectedComponents = [TTJets_LO]
    else:
        selectedComponents = RelVals740
    print "Selecting only one file", getHeppyOption("all")
    if not getHeppyOption("all"):
        for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1
            comp.fineSplitFactor = 1 if getHeppyOption("single") else 4
elif test == '74X-Data':
    from CMGTools.TTHAnalysis.samples.samples_13TeV_74X import *
    from CMGTools.TTHAnalysis.samples.samples_8TeVReReco_74X import *
    what = getHeppyOption("sample")
    if what == "SingleMu":
        selectedComponents = [ SingleMu_740p9 ]
    elif what == "Z":
        selectedComponents = [ SingleMuZ_740p9, DoubleElectronZ_740p9 ]
    elif what == "MuEG":
        selectedComponents = [ MuEG_740p9 ]
    else:
        selectedComponents = dataSamples740p9
    if not getHeppyOption("all"):
        for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1
            comp.fineSplitFactor = 1 if getHeppyOption("single") else 4


## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerSusySingleLepton/tree.root',
    option='recreate'
    )    
outputService.append(output_service)

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
if getHeppyOption("nofetch"):
    event_class = Events 
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = outputService,  
                     events_class = event_class)
