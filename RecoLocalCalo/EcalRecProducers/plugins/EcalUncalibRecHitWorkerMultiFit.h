#ifndef RecoLocalCalo_EcalRecProducers_EcalUncalibRecHitRecWorkerGlobal_hh
#define RecoLocalCalo_EcalRecProducers_EcalUncalibRecHitRecWorkerGlobal_hh

/** \class EcalUncalibRecHitRecGlobalAlgo                                                                                                                                           
 *  Template used to compute amplitude, pedestal using a weights method                                                                                                            
 *                           time using a ratio method                                                                                                                             
 *                           chi2 using express method  
 *
 *  \author R. Bruneliere - A. Zabi
 */

#include "RecoLocalCalo/EcalRecProducers/interface/EcalUncalibRecHitWorkerBaseClass.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalUncalibRecHitMultiFitAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalUncalibRecHitTimeWeightsAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalUncalibRecHitRecChi2Algo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalUncalibRecHitRatioMethodAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalUncalibRecHitLeadingEdgeAlgo.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/EcalObjects/interface/EcalTimeCalibConstants.h"
#include "CondFormats/EcalObjects/interface/EcalTimeOffsetConstant.h"
#include "CondFormats/EcalObjects/interface/EcalPedestals.h"
#include "CondFormats/EcalObjects/interface/EcalGainRatios.h"
#include "CondFormats/EcalObjects/interface/EcalWeightXtalGroups.h"
#include "CondFormats/EcalObjects/interface/EcalTBWeights.h"
#include "CondFormats/EcalObjects/interface/EcalSampleMask.h"


namespace edm {
        class Event;
        class EventSetup;
        class ParameterSet;
}

class EcalUncalibRecHitWorkerMultiFit : public EcalUncalibRecHitWorkerBaseClass {

        public:
                EcalUncalibRecHitWorkerMultiFit(const edm::ParameterSet&);
				//EcalUncalibRecHitWorkerMultiFit(const edm::ParameterSet&);
                virtual ~EcalUncalibRecHitWorkerMultiFit() {};

                void set(const edm::EventSetup& es);
                bool run(const edm::Event& evt, const EcalDigiCollection::const_iterator & digi, EcalUncalibratedRecHitCollection & result);

        protected:

                edm::ParameterSet EcalPulseShapeParameters_;

                double pedVec[3];
		double pedRMSVec[3];
                double gainRatios[3];

                edm::ESHandle<EcalPedestals> peds;
                edm::ESHandle<EcalGainRatios>  gains;

                double timeCorrection(float ampli,
                    const std::vector<float>& amplitudeBins, const std::vector<float>& shiftBins);

                const TMatrixDSym &noisecor(bool barrel, int gain) const;                
                
                // multifit method
                TMatrixDSym noisecorEBg12;
                TMatrixDSym noisecorEEg12;
                TMatrixDSym noisecorEBg6;
                TMatrixDSym noisecorEEg6;
                TMatrixDSym noisecorEBg1;
                TMatrixDSym noisecorEEg1;
                TVectorD fullpulseEB;
                TVectorD fullpulseEE;
                TMatrixDSym fullpulsecovEB;
                TMatrixDSym fullpulsecovEE;
                std::set<int> activeBX;
                bool ampErrorCalculation_;
                EcalUncalibRecHitMultiFitAlgo multiFitMethod_;
                

                // determine which of the samples must actually be used by ECAL local reco
                edm::ESHandle<EcalSampleMask> sampleMaskHand_;                
                
                // time algorithm to be used to set the jitter and its uncertainty
                std::string timealgo_;

                // time weights method
                edm::ESHandle<EcalWeightXtalGroups>  grps;
                edm::ESHandle<EcalTBWeights> wgts;
                const EcalWeightSet::EcalWeightMatrix* weights[2];
                EcalUncalibRecHitTimeWeightsAlgo<EBDataFrame> weightsMethod_barrel_;
                EcalUncalibRecHitTimeWeightsAlgo<EEDataFrame> weightsMethod_endcap_;

                // ratio method
                std::vector<double> EBtimeFitParameters_; 
                std::vector<double> EEtimeFitParameters_; 
                std::vector<double> EBamplitudeFitParameters_; 
                std::vector<double> EEamplitudeFitParameters_; 
                std::pair<double,double> EBtimeFitLimits_;  
                std::pair<double,double> EEtimeFitLimits_;  

                EcalUncalibRecHitRatioMethodAlgo<EBDataFrame> ratioMethod_barrel_;
                EcalUncalibRecHitRatioMethodAlgo<EEDataFrame> ratioMethod_endcap_;

                double EBtimeConstantTerm_;
                double EEtimeConstantTerm_;

                // leading edge method
                edm::ESHandle<EcalTimeCalibConstants> itime;
		edm::ESHandle<EcalTimeOffsetConstant> offtime;
                std::vector<double> ebPulseShape_;
                std::vector<double> eePulseShape_;
                EcalUncalibRecHitLeadingEdgeAlgo<EBDataFrame> leadingEdgeMethod_barrel_;
                EcalUncalibRecHitLeadingEdgeAlgo<EEDataFrame> leadingEdgeMethod_endcap_;


                // chi2 thresholds for flags settings
                bool kPoorRecoFlagEB_;
                bool kPoorRecoFlagEE_;
                double chi2ThreshEB_;
                double chi2ThreshEE_;


 private:
                void fillInputs(const edm::ParameterSet& params);

};

#endif
