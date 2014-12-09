import CMGTools.RootTools.fwlite.Config as cfg
import os

from CMGTools.TTHAnalysis.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec = kreator.makeMCComponentFromEOS('T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec', '/T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/MINIAODSIM/%s')
T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec = kreator.makeMCComponentFromEOS('T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec', '/T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/MINIAODSIM/%s')
T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec = kreator.makeMCComponentFromEOS('T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec', '/T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/MINIAODSIM/%s')
T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec = kreator.makeMCComponentFromEOS('T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec', '/T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/MINIAODSIM/%s')

T1tttt_gluino_1300_LSP_100 = kreator.makeMCComponentFromEOS('T1tttt_gluino_1300_LSP_100', '/13TeV_T1tttt_gluino_1300_LSP_100/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')
T1tttt_gluino_800_LSP_450 = kreator.makeMCComponentFromEOS('T1tttt_gluino_800_LSP_450', '/13TeV_T1tttt_gluino_800_LSP_450/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')
T5qqqqWW_Gl_1400_LSP_100_Chi_325 = kreator.makeMCComponentFromEOS('T5qqqqWW_Gl_1400_LSP_100_Chi_325', '/13TeV_T5qqqqWW_Gl_1400_LSP_100_Chi_325/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')
T5qqqqWW_Gl_1400_LSP_300_Chi_315 = kreator.makeMCComponentFromEOS('T5qqqqWW_Gl_1400_LSP_300_Chi_315', '/13TeV_T5qqqqWW_Gl_1400_LSP_300_Chi_315/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')

SqGltttt_Gl_1300_Sq_1300_LSP_100 = kreator.makeMCComponentFromEOS('SqGltttt_Gl_1300_Sq_1300_LSP_100', '/13TeV_SqGltttt_Gl_1300_Sq_1300_LSP_100/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')
T6qqWW_Sq_950_LSP_300_Chi_350 =kreator.makeMCComponentFromEOS('T6qqWW_Sq_950_LSP_300_Chi_350', '/13TeV_T6qqWW_Sq_950_LSP_300_Chi_350/', '/store/cmst3/group/susy/alobanov/MC/MiniAOD_v2/%s')

allComps = [T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec, T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec, T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec, T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec, T1tttt_gluino_1300_LSP_100, T1tttt_gluino_800_LSP_450, T5qqqqWW_Gl_1400_LSP_100_Chi_325, T5qqqqWW_Gl_1400_LSP_300_Chi_315, SqGltttt_Gl_1300_Sq_1300_LSP_100, T6qqWW_Sq_950_LSP_300_Chi_350]

dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
from CMGTools.TTHAnalysis.setup.Efficiencies import eff2012
for comp in allComps:
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.isMC = True
    comp.isData = False
    comp.efficiency = eff2012

