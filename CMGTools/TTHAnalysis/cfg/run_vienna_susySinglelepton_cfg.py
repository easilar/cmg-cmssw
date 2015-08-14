##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES         ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

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
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
jetAna.minLepPt = 10
#jetAna.jetPt = 25
#jetAna.jetEta = 2.4

jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets =  True #For data

metAna.recalibrate = False #should be false in susycore, already

isoTrackAna.setOff=False
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

from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheFilterAna = cfg.Analyzer(
    hbheAnalyzer, name = 'hbheAnalyzer',
)

susyCoreSequence.insert(-1, hbheFilterAna)

### Single lepton + ST skim
#from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
#ttHSTSkimmer = cfg.Analyzer(
#    ttHSTSkimmer, name='ttHSTSkimmer',
#    minST = 200,
#    )

#from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer import ttHReclusterJetsAnalyzer
#ttHReclusterJets = cfg.Analyzer(
#    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
#    pTSubJet = 30,
#    etaSubJet = 5.0,
#            )

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import * # central trigger list
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
triggerFlagsAna.triggerBits = {
        # put trigger here for _MC_
        ## hadronic
        'HT350' : triggers_HT350,
        'HT600' : triggers_HT600,
        'HT900' : triggers_HT900,
        'MET170' : triggers_MET170,
        'HTMET' : triggers_HTMET,
        'Had' : triggers_had,
        ## muon
        'SingleMu' : triggers_1mu,
        'Mu45NoIso' : trigger_1mu_noiso_r,
        'Mu50NoIso' : trigger_1mu_noiso_w,
        'MuHT600' : triggers_mu_ht600,
        'MuHT400MET70' : triggers_mu_ht400_met70,
        'MuHT350MET70' : triggers_mu_ht350_met70,
        'MuMET120' : triggers_mu_met120,
        'MuHT400B': triggers_mu_ht400_btag,
        'MuHad' : triggers_muhad,
        ## electrons
        'SingleEl' : triggers_1el,
        'ElNoIso' : trigger_1el_noiso,
        'EleHT600' : triggers_el_ht600,
        'EleHT400MET70' : triggers_el_ht400_met70,
        'EleHT350MET70' : triggers_el_ht350_met70,
        'EleHT200' :triggers_el_ht200,
        'ElHT400B': triggers_el_ht400_btag,
        'ElHad' : triggers_elhad,
        #put trigger here for data
#        'mumuRun1' : triggers_mumu_run1,
        'mumuIso' : triggers_mumu_iso,
        'mumuNoniso_50ns' : triggers_mumu_noniso_50ns,
        'mumuNoiso' : triggers_mumu_noniso,
        'mumuSS' : triggers_mumu_ss,
        'mumuHT' : triggers_mumu_ht,
#
        'MET170_pres'      :triggers_MET170_pres   , 
        'MET250'           :triggers_MET250        ,
        'MET90nc'          :triggers_MET90nc       ,
        'MET120nc'         :triggers_MET120nc      ,
        'MET90'            :triggers_MET90MHT90    ,
        'MET120'           :triggers_MET120MHT120  ,
        'PhysRates'        :triggers_PhysRate      ,
        'DiPFJet140': ["HLT_DiPFJetAve140_v*"],
        'DiPFJet200': ["HLT_DiPFJetAve200_v*"],
        'DiPFJet260': ["HLT_DiPFJetAve260_v*"],
        'DiPFJet320': ["HLT_DiPFJetAve320_v*"],
        'DiPFJet400': ["HLT_DiPFJetAve400_v*"],
        'DiPFJet500': ["HLT_DiPFJetAve500_v*"],
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

#!# #-------- SAMPLES AND TRIGGERS -----------

selectedComponents = [
        ]

sequence = cfg.Sequence(
  susyCoreSequence+
      [ ttHEventAna,
        treeProducer,
        ])

isData = True
removeResiduals = False
bx = '50ns'
#bx = '25ns'

if isData:
  test="data"
else:
  if bx=='50ns':test=3
  if bx=='25ns':test=5

#if True or getHeppyOption("loadSamples"):
if getHeppyOption("loadSamples"):
  from CMGTools.RootTools.samples.samples_13TeV_74X import *
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
    # RelVal test 
    selectedComponents=[ZMM_746p1_bx50]
    for comp in selectedComponents:
      comp.splitFactor = 1 
  elif test==4:
#    TTJets_50ns.fineSplitFactor = 4
#    selectedComponents = [TTJets_50ns]
#    selectedComponents = [DYJetsToLL_M50_50ns, DYJetsToLL_M10to50_50ns, WJetsToLNu_50ns]
    selectedComponents = [TTJets]
    for comp in selectedComponents:
      comp.files = comp.files[:1]
      comp.splitFactor = len(comp.files)
  elif test==5:
    selectedComponents = [DYJetsToLL_M50]
#    selectedComponents = [WJetsToLNu_HT600to800,WJetsToLNu_HT800to1200,WJetsToLNu_HT1200to2500,WJetsToLNu_HT2500toInf]
    for comp in selectedComponents:
      comp.files = comp.files[:]
      comp.splitFactor = len(comp.files) 

  elif test=="data":
    from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
    selectedComponents = [ SingleMuon_Run2015B ]
    for comp in selectedComponents:
        comp.splitFactor = 1
#        comp.files = ["root://eoscms.cern.ch//store/data/Run2015B/DoubleEG/MINIAOD/PromptReco-v1/000/251/096/00000/8A2D533C-5626-E511-AF3C-02163E011FAB.root"]
        comp.files = comp.files[:1] 
        comp.isMC = False
        comp.isData = True
#        comp.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.json"


if isData:
  assert bx!='25ns', "Has the future arrived?"
  jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_50nsV4_DATA.db'
  jecEra    = 'Summer15_50nsV4_DATA'
  mcGT = 'XXX'
  dataGT= '74X_dataRun2_Prompt_v1' #50ns data
  jetAna.mcGT     = "Summer15_50nsV4_MC"
  jetAna.dataGT   = "Summer15_50nsV4_DATA"
  eventFlagsAna.processName = 'RECO'
  metAnaDef.metCollection   = ("slimmedMETs","", "RECO")
  jetAna.applyL2L3Residual = False if removeResiduals else 'Data' 
else: #simulation
  if bx=='50ns':
    jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_50nsV2_MC.db'
    jecEra    = 'Summer15_50nsV2_MC'
    mcGT= 'MCRUN2_74_V9A' #50ns MC
    dataGT= 'XXX' #50ns Data
    jetAna.mcGT     = "Summer15_50nsV3_MC"
    jetAna.dataGT   = "XXX"#"Summer15_50nsV2"
  if bx=='25ns':
    jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV2_MC.db'
#    jecDBFile = ''
    jecEra    = 'Summer15_25nsV2_MC' 
    dataGT= 'XXX' #50ns Data
    mcGT= 'MCRUN2_74_V9' #25ns MC
    jetAna.mcGT     = "Summer15_25nsV2_MC"
    jetAna.dataGT   = "XXX" 

GT = dataGT if isData else mcGT
preprocessorFilename = "MetType1_jec_%s_GT_%s_residuals_%s.py"%(jecEra, GT, str(not(removeResiduals)))

# -------------------- Running pre-processor
if getHeppyOption("makePreProcessorFile"): #create preprocessor file on the fly
  import subprocess
  extraArgs=[]
  if isData:
    extraArgs.append('--isData')
  if removeResiduals:extraArgs.append('--removeResiduals')
  preprocessorDir = "$CMSSW_BASE/tmp"
  preprocessorFile = "/".join([preprocessorDir, preprocessorFilename])
  args = ['python', 
    os.path.expandvars('$CMSSW_BASE/python/CMGTools/ObjectStudies/corMETMiniAOD_cfgCreator.py'),\
    '--GT='+GT, 
    '--outputFile='+preprocessorFile, 
    '--jecDBFile='+jecDBFile,
    '--jecEra='+jecEra
    ] + extraArgs 
  #print "Making pre-processorfile:"
  #print " ".join(args)
  subprocess.call(args)
else: #use precomputed preprocessor files
  preprocessorDir = "$CMSSW_BASE/python/CMGTools/TTHAnalysis/preProcFiles"
  preprocessorFile = "/".join([preprocessorDir, preprocessorFilename])

print "Using preprocessorFile", preprocessorFile

from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor(preprocessorFile)

from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
event_class = Events
if getHeppyOption("fetch"):
  event_class = EOSEventsWithDownload

#printComps(config.components, True)
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

