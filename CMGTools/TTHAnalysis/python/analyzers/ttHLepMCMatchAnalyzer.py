import operator 
import itertools
import copy
from math import *

from ROOT import TLorentzVector

from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.Event import Event
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.Lepton import Lepton
from CMGTools.RootTools.physicsobjects.Photon import Photon
from CMGTools.RootTools.physicsobjects.Electron import Electron
from CMGTools.RootTools.physicsobjects.Muon import Muon
from CMGTools.RootTools.physicsobjects.Jet import Jet

from CMGTools.RootTools.utils.DeltaR import *
from CMGTools.RootTools.physicsobjects.genutils import *

class ttHLepMCMatchAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHLepMCMatchAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(ttHLepMCMatchAnalyzer, self).declareHandles()

    def beginLoop(self):
        super(ttHLepMCMatchAnalyzer,self).beginLoop()

    def matchLeptons(self, event):
        def plausible(rec,gen):
            if abs(rec.pdgId()) == 11 and abs(gen.pdgId()) != 11:   return False
            if abs(rec.pdgId()) == 13 and abs(gen.pdgId()) != 13:   return False
            dr = deltaR(rec.eta(),rec.phi(),gen.eta(),gen.phi())
            if dr < 0.3: return True
            if rec.pt() < 10 and abs(rec.pdgId()) == 13 and gen.pdgId() != rec.pdgId(): return False
            if dr < 0.7: return True
            if min(rec.pt(),gen.pt())/max(rec.pt(),gen.pt()) < 0.3: return False
            return True

        leps = event.selectedLeptons[:]
        if hasattr(self.cfg_ana,'matchAllInclusiveLeptons') and self.cfg_ana.matchAllInclusiveLeptons:
            leps = event.inclusiveLeptons[:]
        match = matchObjectCollection3(leps, 
                                       event.genleps + event.gentauleps, 
                                       deltaRMax = 1.2, filter = plausible)
        for lep in leps:
            gen = match[lep]
            lep.mcMatchId = (gen.sourceId if gen != None else 0)
            lep.mcMatchTau = (gen.isTau if gen != None else -99)

    def isFromB(self,particle,bid=5, done={}):
        for i in xrange( particle.numberOfMothers() ): 
            mom  = particle.mother(i)
            momid = abs(mom.pdgId())
            if momid / 1000 == bid or momid / 100 == bid or momid == bid: 
                return True
            elif mom.status() == 2 and self.isFromB(mom, done=done):
                return True
        return False

    def sourceBQuark(self,particle,event):
        for i in xrange( particle.numberOfMothers() ):
            mom  = particle.mother(i)
            if mom.status() >= 3 and abs(mom.pdgId()) == 5:
                return mom
            elif mom.status() == 2:
                momB = self.sourceBQuark(mom,event)
                if momB != None: return momB
        return None
                
    def matchAnyLeptons(self, event): 
        event.anyLeptons = [ x for x in event.genParticles if x.status() == 1 and abs(x.pdgId()) in [11,13] ]
        leps = event.inclusiveLeptons if hasattr(event, 'inclusiveLeptons') else event.selectedLeptons
        match = matchObjectCollection3(leps, event.anyLeptons, deltaRMax = 0.3, filter = lambda x,y : abs(x.pdgId()) == abs(y.pdgId()))
        for lep in leps:
            gen = match[lep]
            lep.mcMatchAny_gp = gen
            lep.mcMatchAny = ((1 + self.isFromB(gen)) if gen != None else 0)
            if lep.mcMatchAny == 1 and self.isFromB(gen,bid=4):
                lep.mcMatchAny2 = 4
            else:
                lep.mcMatchAny2 = (5 if lep.mcMatchAny == 2 else lep.mcMatchAny)
            if gen != None and hasattr(lep,'mcMatchId') and lep.mcMatchId == 0:
                if isPromptLepton(gen, False): lep.mcMatchId = 100
            elif not hasattr(lep,'mcMatchId'):
                lep.mcMatchId = 0
            if not hasattr(lep,'mcMatchTau'): lep.mcMatchTau = 0
            lep.mcDeltaRB  = 999
            if gen != None:
                bgen = self.sourceBQuark(gen,event)
                if bgen != None:
                    lep.mcDeltaRB = deltaR(bgen.eta(),bgen.phi(),lep.eta(),lep.phi())

    def doLeptonSF(self, event):
        eff, effUp, effDn = [1.],[1.],[1.]
        for l in event.selectedLeptons:
            eff.append(eff[-1]*l.eff)
            effUp.append(effUp[-1]*l.effUp)
            effDn.append(effDn[-1]*l.effDwn)
        for i in 1,2,3,4:
            setattr(event, 'LepEff_%dlep'%i,      eff[min(i,len(eff)-1)])
            setattr(event, 'LepEffUp_%dlep'%i,  effUp[min(i,len(eff)-1)])
            setattr(event, 'LepEffDn_%dlep'%i,  effDn[min(i,len(eff)-1)])

    def process(self, iEvent, event):

        # if not MC, nothing to do
        if not self.cfg_comp.isMC: 
            return True

        self.matchLeptons(event)

        self.matchAnyLeptons(event)

        self.doLeptonSF(event)

        return True
