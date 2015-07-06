##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES       ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *


# Lepton Preselection
# ele
lepAna.loose_electron_id = "POG_MVA_ID_Run2_NonTrig_Loose"
lepAna.loose_electron_pt  = 5
# mu
lepAna.loose_muon_pt  = 5

# Redefine what I need
lepAna.packedCandidates = 'packedPFCandidates'

# selec Iso
isolation = "miniIso"

if isolation == "miniIso":
# do miniIso
	lepAna.doMiniIsolation = True
	lepAna.miniIsolationPUCorr = 'rhoArea'
	lepAna.miniIsolationVetoLeptons = None
	lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
	lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
# normal relIso03
	lepAna.ele_isoCorr = "rhoArea"
	lepAna.mu_isoCorr = "rhoArea"

	lepAna.loose_electron_relIso = 0.5
	lepAna.loose_muon_relIso = 0.5

# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 1
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
jetAna.minLepPt = 10

jetAna.mcGT = "Summer15_V5_MC"
jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets = True #should be true in susycore, already
metAna.recalibrate = False #should be false in susycore, already

isoTrackAna.setOff=False

# store all taus by default
genAna.allGenTaus = True

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
	ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
	minJets25 = 0,
	)

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
						ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
						ttHSVAna)

## Single lepton + ST skim
from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
ttHSTSkimmer = cfg.Analyzer(
	ttHSTSkimmer, name='ttHSTSkimmer',
	minST = 200,
	)

from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer import ttHReclusterJetsAnalyzer
ttHReclusterJets = cfg.Analyzer(
	ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
	pTSubJet = 30,
	etaSubJet = 5.0,
			)

from CMGTools.RootTools.samples.triggers_13_TeV_Spring15_1l import *

triggerFlagsAna.triggerBits = {
#put trigger here for data
	'HT350' : triggers_HT350,
	'HT900' : triggers_HT900,
	'MET170' : triggers_MET170,
	'HTMET' : triggers_HTMET,
	'SingleMu' : triggers_ref_mu,
	'SingleEl' : triggers_ref_el,
	'MuHT600' : triggers_mu_ht600,
	'MuHT400MET70' : triggers_mu_ht400_met70,
	'MuMET120' : triggers_mu_met120,
	'EleHT600' : triggers_el_ht600,
	'EleHT400MET70' : triggers_el_ht400_met70,
	'EleHT200' :triggers_el_ht200
}

# Tree Producer
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



#-------- SAMPLES AND TRIGGERS -----------

# -- old PHYS14
#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
#selectedComponents = [QCD_HT_100To250, QCD_HT_250To500, QCD_HT_500To1000, QCD_HT_1000ToInf,TTJets, TTWJets, TTZJets, TTH, SMS_T1tttt_2J_mGl1500_mLSP100, SMS_T1tttt_2J_mGl1200_mLSP800] + SingleTop + WJetsToLNuHT + DYJetsM50HT + T5ttttDeg + T1ttbbWW + T5qqqqWW

# -- new 74X samples
from CMGTools.TTHAnalysis.samples.samples_13TeV_74X import *

selectedComponents = [
#TTJets,
#TTJets_50ns
TTJets_LO,
#TTJets_LO_50ns
]


#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
	ttHEventAna,
	#ttHSTSkimmer,
	ttHReclusterJets,
	treeProducer,
	])


#-------- HOW TO RUN
test = 3
if test==1:
	# test a single component, using a single thread.
	comp = TTJets
	comp.files = comp.files[:1]
	selectedComponents = [comp]
	comp.splitFactor = 1
elif test==2:
	# test all components (1 thread per component).
	for comp in selectedComponents:
		comp.splitFactor = 1
		comp.fineSplitFactor = 10
		comp.files = comp.files[:1]
elif test==3:
	# run all components (1 thread per component).
	for comp in selectedComponents:
		comp.splitFactor = len(comp.files)

elif test=="data":
	from CMGTools.TTHAnalysis.samples.samples_13TeV_Data import *
	selectedComponents = [ privEGamma2015A ]

	for comp in selectedComponents:
		comp.splitFactor = 1
		comp.fineSplitFactor = 1
		comp.files = comp.files[:1]


from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
					 sequence = sequence,
					 services = [],
					 events_class = Events)
