#-------- SAMPLES AND TRIGGERS -----------

from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
selectedComponents =  [TTJets]
#TTJets.splitFactor=1000
from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
selectedComponents = [T2DegStop_300_270]


from CMGTools.TTHAnalysis.samples.samples_13TeV_private_heplx import *
selectedComponents = [DYJetsToLL_M50_PU20bx25]#, DYJetsToLLHT100to200_M50_PU20bx25, DYJetsToLLHT200to400_M50_PU20bx25, DYJetsToLLHT400to600_M50_PU20bx25, DYJetsToLLHT600toInf_M50_PU20bx25]

#selectedComponents = [ TT_PU40bx25 ]
#selectedComponents = [ TT_PU4bx50 ]

#-------- HOW TO RUN
test = 2
print "selectedComponents1 ",selectedComponents
if test==1:
    # test a single component, using a single thread.
    #comp = TTJets
    comp = T2DegStop_300_270
#    comp = SMS_T1tttt_2J_mGl1500_mLSP100
    comp.files = comp.files[:10]
    print "Files:",comp.files
    selectedComponents = [comp]
    comp.splitFactor = 1
elif test==2:
    # test all components (1 thread per component).
    print "selectedComponents2a ",selectedComponents
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:1]
    print "selectedComponents2b ",selectedComponents#

