########################################
# v532_optima_base
# Atasoy et al., 2013
########################################

############ MODEL 4 ###################

# The model 4 includes two extra non-linear specifications (we already have the piecewise formulation for B_DIST from Model_3) under the form of a box cox
# on the time spent in public transport or in the car (private transport). The hypothesis is that as the time duration increases,
# the marginal impact of time on the utility probably decreases. For example, 5 extra minutes on a 2-hour long trip will be less annoying than on a 10-min trip.
# A lambda value lower than 1 implies that the marginal cost of time decreases with the duration, whereas a lambda value greater than 1 means that it increases with the duration
# (which would be nonsensical and wouldn't pass the informal test).

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS

ASC_CAR = Beta('ASC_CAR',-0.392432,-10000,10000,1,'ASC_CAR' )
BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',-0.537653,-10000,10000,1,'BETA_COST_SHARE_CAR' )
BETA_TIME_CAR = Beta('BETA_TIME_CAR',-0.116882,-10000,10000,1,'BETA_TIME_CAR' )
LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',0.634672,-1000,1000,1,'LAMBDA_TIME_CAR' )
BETA_NbCar = Beta('BETA_NbCar',1.20729,-10000,10000,1,'BETA_NbCar' )
BETA_NbChild = Beta('BETA_NbChild',0.194942,-10000,10000,1,'BETA_NbChild' )
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0.99994,-10000,10000,1,'BETA_LANGUAGE' )
BETA_WorkTrip = Beta('BETA_WorkTrip',-0.487827,-10000,10000,1,'BETA_WorkTrip' )
BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',-0.282421,-10000,10000,1,'BETA_COST_SHARE_PT' )
BETA_TIME_PT = Beta('BETA_TIME_PT',-0.0171339,-10000,10000,1,'BETA_TIME_PT' )
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',0.950997,-1000,1000,1,'LAMBDA_TIME_PT' )
BETA_Urban = Beta('BETA_Urban',0.222714,-10000,10000,1,'BETA_Urban' )
BETA_Student = Beta('BETA_Student',3.28702,-10000,10000,1,'BETA_Student' )
ASC_SM = Beta('ASC_SM',-0.214546,-10000,10000,1,'ASC_SM' )
ASC_DIST = Beta('ASC_DIST',-10.0599,-10000,10000,1,'ASC_DIST' )
BETA_DIST_YOUNG = Beta('BETA_DIST_YOUNG',0.543686,-10000,10000,1,'BETA_DIST_YOUNG' )
BETA_DIST_ADULT = Beta('BETA_DIST_ADULT',0.00173394,-10000,10000,1,'BETA_DIST_ADULT' )
BETA_DIST_OLD = Beta('BETA_DIST_OLD',-0.0314759,-10000,10000,1,'BETA_DIST_OLD' )
BETA_Nbikes = Beta('BETA_Nbikes',0.305972,-10000,10000,1,'BETA_Nbikes' )


# VARIABLES

one = DefineVariable('one',1)
FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

Age = DefineVariable('Age', 2010 - BirthYear)
AgeYoung = DefineVariable('AgeYoung', (Age > 18) * 18 + Age * (Age <= 18))
AgeAdult = DefineVariable('AgeAdult', (Age > 65) * (65 - 18) + (Age - 18) * (18 < Age <= 65))
AgeOld = DefineVariable('AgeOld', (Age > 65) * (Age - 65))

ApproxIncome = DefineVariable('ApproxIncome', (Income == -1) * 7000 + (Income == 1) * 2500 + (Income == 2) * 3250 + (Income==3) * 5000 + (Income == 4) * 7000 + (Income == 5) * 9000 + (Income == 6) * 10000)
#CostCarShare_norm = DefineVariable('CostCarShare_norm', CostCarCHF * 1000/ApproxIncome)
#CostPTShare_norm = DefineVariable('CostPTShare_norm', MarginalCostPT * 1000/ApproxIncome)

# Need to know explicitly how CostCarShare_norm and CostPtShare_norm depend 
# on CostCarCHF and MarginalCostPT respectively

CostCarShare_norm = CostCarCHF * 1000/ApproxIncome
CostPTShare_norm = MarginalCostPT * 1000/ApproxIncome

# Variables for simulation

#CostCarShare_norm_increased = DefineVariable('CostCarShare_norm', (1.1*CostCarCHF)*1000/ApproxIncome)
#CostPTShare_norm_increased = DefineVariable('CostPTShare_norm_increased', (1.1*MarginalCostPT)*1000/ApproxIncome)

# UTILITIES

CAR = ASC_CAR * one + BETA_COST_SHARE_CAR * CostCarShare_norm + BETA_TIME_CAR * ((TimeCar ** LAMBDA_TIME_CAR) - 1)/LAMBDA_TIME_CAR + BETA_NbCar * NbCars + BETA_NbChild * NbChildren + BETA_LANGUAGE * FrenchRegion + BETA_WorkTrip * WORK

PT = BETA_COST_SHARE_PT * CostPTShare_norm + BETA_TIME_PT * ((TimePT ** LAMBDA_TIME_PT) - 1)/LAMBDA_TIME_PT + BETA_Urban * URBAN + BETA_Student * STUDENT

SM = ASC_SM * one + (ASC_DIST + BETA_DIST_YOUNG * AgeYoung + BETA_DIST_ADULT * AgeAdult + BETA_DIST_OLD * AgeOld) * distance_km  + BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}

# EXCLUDE
BIOGEME_OBJECT.EXCLUDE = (Choice == -1) + (BirthYear == -1) + (Income == -1) # I exclude the respondents whose age we can not calculate or whose income we don't know

# Logit, with availability conditions
prob_CAR = bioLogit(V,av,1)
prob_PT = bioLogit(V, av,0)
prob_SM = bioLogit(V,av,2)


# Defines an itertor on the data
rowIterator('obsIter')

# Calculate the value of time for the alternatives, in CHF/hour
VOT_CAR = 60*Derive(CAR, 'TimeCar')/Derive(CAR, 'CostCarCHF')
VOT_PT  = 60*Derive(PT, 'TimePT')/Derive(PT, 'MarginalCostCHF')


normalization_PT = 464.807
normalization_CAR = 968.884
# Calculate cost elasticity for different alternatives
elas_CAR_cost = Derive(prob_CAR, 'CostCarCHF')*CostCarCHF/prob_CAR
elas_PT_cost = Derive(prob_PT, 'MarginalCostPT')*MarginalCostPT/prob_PT


#Define the weight
sampleSize = 1524
theWeight = Weight*sampleSize/0.617062
BIOGEME_OBJECT.WEIGHT = theWeight

# What has to be calculated?
simulate = {'01 Disag. Elast. CAR - Cost': elas_CAR_cost,
	    '02 Disag. Elast. PT - Cost': elas_PT_cost,
	    '03 Agg. Elast. CAR - Cost': elas_CAR_cost*prob_CAR/normalization_CAR,
	    '04 Agg. Elast. PT - Cost': elas_PT_cost*prob_PT/normalization_PT,
	    '05 VoT CAR': VOT_CAR,
	    '06 VoT PT': VOT_PT}

BIOGEME_OBJECT.SIMULATE = Enumerate(simulate,'obsIter')


# Optimization algorithm
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"

# Print some statistics:
nullLoglikelihood(av,'obsIter')
choiceSet = [1,2,0]
cteLoglikelihood(choiceSet,Choice,'obsIter')
availabilityStatistics(av,'obsIter')
BIOGEME_OBJECT.FORMULAS['Car utility'] = CAR
BIOGEME_OBJECT.FORMULAS['PT utility'] = PT
BIOGEME_OBJECT.FORMULAS['SM utility'] = SM


## Code for the sensitivity analysis
#names = ['ASC_CAR','ASC_DIST','ASC_SM','BETA_COST_SHARE_CAR','BETA_COST_SHARE_PT','BETA_DIST_ADULT','BETA_DIST_OLD','BETA_DIST_YOUNG','BETA_LANGUAGE','BETA_NbCar','BETA_NbChild','BETA_Nbikes','BETA_Student','BETA_TIME_CAR','BETA_TIME_PT','BETA_Urban','BETA_WorkTrip','LAMBDA_TIME_CAR','LAMBDA_TIME_PT']
#values = [[0.0611499,-0.0335913,0.02671,-0.00136788,0.0015453,-1.54104e-05,0.000155702,0.00184966,-0.0013099,-0.0193541,-0.000830768,0.000135233,-0.0182512,-0.00211749,0.000737684,0.0082492,-0.00341747,-0.00457145,0.00850798],[-0.0335913,7.8333,-0.0125775,0.00615212,-0.00231066,0.00285466,-0.00687336,-0.439444,0.0215117,0.0372431,-0.0116161,-0.0101041,0.299452,0.0154167,0.00397695,-0.00377924,0.00569628,0.0152322,0.0299759],[0.02671,-0.0125775,0.174228,0.00611209,0.00251386,-0.00011318,-0.000295423,-0.000200937,-0.000928631,0.000959076,-0.000938762,-0.0132999,0.0118171,-0.0101513,-0.00148832,0.00784735,-0.00165086,-0.0157705,-0.0136645],[-0.00136788,0.00615215,0.00611209,0.0411667,0.00874279,-5.06044e-06,1.55414e-05,-0.00033574,-0.00336581,0.00426468,0.000883373,-0.000375617,-0.000453003,-0.0020968,-0.000619989,0.000569752,-3.74201e-05,-0.00335992,-0.0114343],[0.0015453,-0.00231065,0.00251386,0.00874279,0.00550797,-1.82054e-06,1.00107e-05,0.000146034,-0.000425919,0.00107476,-0.000123518,-0.000259251,-0.00189851,-0.000579117,-9.30644e-05,-0.000333548,-0.000864137,-0.00226568,-0.00214382],[-1.54104e-05,0.00285466,-0.00011318,-5.06044e-06,-1.82054e-06,5.49645e-06,-1.28347e-05,-0.000167593,-2.99576e-05,2.69576e-05,-3.41686e-05,3.08474e-05,0.00019891,1.67025e-05,4.28774e-06,-3.05816e-05,-6.14135e-06,1.82905e-05,3.63064e-05],[0.000155702,-0.00687336,-0.000295423,1.55414e-05,1.00107e-05,-1.28347e-05,0.000157601,0.00040281,0.000212557,-7.87165e-05,5.06694e-05,3.87833e-05,-0.000486885,-5.68329e-05,-1.28662e-05,8.95803e-05,-3.91889e-05,-7.17865e-05,-0.000114339],[0.00184966,-0.439447,-0.000200937,-0.000335739,0.000146034,-0.000167593,0.00040281,0.0246785,-0.00112436,-0.0021468,0.000695821,0.000507374,-0.0172702,-0.000733403,-0.000196096,0.000246615,-0.000284504,-0.00065632,-0.00142721],[-0.0013099,0.0215117,-0.000928631,-0.00336581,-0.000425919,-2.99576e-05,0.000212557,-0.00112436,0.0309054,-0.00108103,-0.000515474,-0.000103647,-0.000211964,0.000375836,6.0902e-05,0.00509541,-0.000858087,0.000661568,0.00105159],[-0.0193541,0.0372431,0.000959076,0.00426468,0.00107476,2.69576e-05,-7.87165e-05,-0.0021468,-0.00108103,0.016449,-0.000573316,0.000265823,0.0146963,-0.000491407,-0.000186942,-0.000783322,-0.00323623,-0.000742245,-0.00244968],[-0.000830768,-0.0116161,-0.000938762,0.000883373,-0.000123518,-3.41686e-05,5.06694e-05,0.000695821,-0.000515474,-0.000573316,0.00518217,0.00101753,0.00143048,-0.000224677,-2.92601e-05,0.00055645,-9.11783e-05,-0.00014013,-0.000270912],[0.000135233,-0.0101041,-0.0132999,-0.000375617,-0.000259251,3.08474e-05,3.87833e-05,0.000507374,-0.000103647,0.000265823,0.00101753,0.00441425,0.00264533,-8.59335e-05,2.1705e-06,0.000191541,-0.000342123,-0.000118263,5.21076e-05],[-0.0182512,0.299452,0.0118171,-0.000453003,-0.00189851,0.00019891,-0.000486885,-0.0172702,-0.000211964,0.0146963,0.00143048,0.00264533,0.182481,-0.00343699,-0.000865327,-0.00458354,-0.000478193,-0.00495412,-0.00860354],[-0.00211749,0.0154167,-0.0101513,-0.0020968,-0.000579117,1.67025e-05,-5.68329e-05,-0.000733403,0.000375836,-0.000491407,-0.000224677,-8.59335e-05,-0.00343699,0.0028781,0.000532493,-0.000281594,0.00010901,0.00491367,0.00545166],[0.000737684,0.00397695,-0.00148832,-0.000619989,-9.30644e-05,4.28774e-06,-1.28662e-05,-0.000196096,6.0902e-05,-0.000186942,-2.92601e-05,2.1705e-06,-0.000865327,0.000532493,0.00016257,-0.00013815,0.000108811,0.000854863,0.00176625],[0.0082492,-0.00377924,0.00784735,0.000569752,-0.000333548,-3.05816e-05,8.95803e-05,0.000246615,0.00509541,-0.000783322,0.00055645,0.000191541,-0.00458354,-0.000281594,-0.00013815,0.0186408,-0.000844553,-0.000118006,-0.00134817],[-0.00341747,0.00569628,-0.00165086,-3.74201e-05,-0.000864137,-6.14135e-06,-3.91889e-05,-0.000284504,-0.000858087,-0.00323623,-9.11783e-05,-0.000342123,-0.000478193,0.00010901,0.000108811,-0.000844553,0.0168439,0.00067488,0.00143461],[-0.00457145,0.0152322,-0.0157705,-0.00335992,-0.00226568,1.82905e-05,-7.17865e-05,-0.00065632,0.000661568,-0.000742245,-0.00014013,-0.000118263,-0.00495412,0.00491367,0.000854863,-0.000118006,0.00067488,0.0106751,0.010011],[0.00850798,0.0299759,-0.0136645,-0.0114343,-0.00214382,3.63064e-05,-0.000114339,-0.00142721,0.00105159,-0.00244968,-0.000270912,5.21076e-05,-0.00860354,0.00545166,0.00176625,-0.00134817,0.00143461,0.010011,0.0209512]]

#vc = bioMatrix(19,names,values)
#BIOGEME_OBJECT.VARCOVAR = vc