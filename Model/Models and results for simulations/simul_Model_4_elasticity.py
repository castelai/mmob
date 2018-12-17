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

ASC_CAR = Beta('ASC_CAR',-0.23312,-10000,10000,1,'ASC_CAR' )
BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',-0.487878,-10000,10000,1,'BETA_COST_SHARE_CAR' )
BETA_TIME_CAR = Beta('BETA_TIME_CAR',-0.361698,-10000,10000,1,'BETA_TIME_CAR' )
LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',0.412394,-1000,1000,1,'LAMBDA_TIME_CAR' )
BETA_NbCar = Beta('BETA_NbCar',1.20093,-10000,10000,1,'BETA_NbCar' )
BETA_NbChild = Beta('BETA_NbChild',0.198291,-10000,10000,1,'BETA_NbChild' )
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0.968596,-10000,10000,1,'BETA_LANGUAGE' )
BETA_WorkTrip = Beta('BETA_WorkTrip',-0.546375,-10000,10000,1,'BETA_WorkTrip' )
BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',-0.272179,-10000,10000,1,'BETA_COST_SHARE_PT' )
BETA_TIME_PT = Beta('BETA_TIME_PT',-0.0841916,-10000,10000,1,'BETA_TIME_PT' )
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',0.67019,-1000,1000,1,'LAMBDA_TIME_PT' )
BETA_Urban = Beta('BETA_Urban',0.206689,-10000,10000,1,'BETA_Urban' )
BETA_Student = Beta('BETA_Student',3.32471,-10000,10000,1,'BETA_Student' )
ASC_SM = Beta('ASC_SM',-0.0444022,-10000,10000,1,'ASC_SM' )
BETA_DIST = Beta('BETA_DIST',-1.44581,-10000,10000,1,'BETA_DIST' )
LAMBDA_DIST = Beta('LAMBDA_DIST',0.223513,-1000,1000,1,'LAMBDA_DIST' )
BETA_Nbikes = Beta('BETA_Nbikes',0.381172,-10000,10000,1,'BETA_Nbikes' )


# VARIABLES

one = DefineVariable('one',1)
FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

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

SM = ASC_SM * one + BETA_DIST * ((distance_km**LAMBDA_DIST)-1)/LAMBDA_DIST  + BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}

# EXCLUDE
BIOGEME_OBJECT.EXCLUDE = (Choice == -1) + (Income == -1)# I exclude the respondents whose age we can not calculate or whose income we don't know

# Logit, with availability conditions
prob_CAR = bioLogit(V,av,1)
prob_PT = bioLogit(V, av,0)
prob_SM = bioLogit(V,av,2)


# Defines an itertor on the data
rowIterator('obsIter')

# Calculate the value of time for the alternatives, in CHF/hour
VOT_CAR = 60*BETA_TIME_CAR*(TimeCar)**(LAMBDA_TIME_CAR-1)*ApproxIncome/(1000*BETA_COST_SHARE_CAR)
VOT_PT  = 60*BETA_TIME_PT*(TimePT)**(LAMBDA_TIME_PT-1)*ApproxIncome/(1000 * BETA_COST_SHARE_PT)

normalization_PT = 480.155
normalization_CAR = 979.301
# Calculate cost elasticity for different alternatives
elas_CAR_cost = Derive(prob_CAR, 'CostCarCHF')*CostCarCHF/prob_CAR
elas_PT_cost = Derive(prob_PT, 'MarginalCostPT')*MarginalCostPT/prob_PT


#Identify groups with lower / higher cost elasticity. Can start by looking at different income  
#brackets.
HighIncome = ((Income == 6) + (Income == 5))
MediumIncome = ((Income == 4) + (Income == 3))
LowIncome = ((Income == 2) + (Income == 1))
elas_PT_cost_high_income = elas_PT_cost*HighIncome
elas_PT_cost_medium_income = elas_PT_cost*MediumIncome
elas_PT_cost_low_income = elas_PT_cost*LowIncome
elas_CAR_cost_high_income = elas_CAR_cost*HighIncome
elas_CAR_cost_medium_income = elas_CAR_cost*MediumIncome
elas_CAR_cost_low_income = elas_CAR_cost*LowIncome

#Define the weight
sampleSize = 1550
theWeight = Weight*sampleSize/0.64176
BIOGEME_OBJECT.WEIGHT = theWeight

# What has to be calculated?
simulate = {'01 Disag. Elast. Car - Cost': elas_CAR_cost,
	    '02 Disag. Elast. Car - Cost, low income': elas_CAR_cost_low_income,
	    '03 Disag. Elast. Car - Cost, medium income': elas_CAR_cost_medium_income,
	    '04 Disag. Elast. Car - Cost, high income': elas_CAR_cost_high_income,
	    '05 Disag. Elast. PT - Cost': elas_PT_cost,
	    '06 Disag. Elast. PT - Cost, low income': elas_PT_cost_low_income,
	    '07 Disag. Elast. PT - Cost, medium income': elas_PT_cost_medium_income,
	    '08 Disag. Elast. PT - Cost, high income': elas_PT_cost_high_income,
	    '09 Agg. Elast. CAR - Cost': elas_CAR_cost*prob_CAR/normalization_CAR,
	    '10 Agg. Elast. PT - Cost': elas_PT_cost*prob_PT/normalization_PT,
	    '11 VoT CAR': VOT_CAR,
	    '12 VoT PT': VOT_PT
}

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
#names = ['ASC_CAR','ASC_SM','BETA_COST_SHARE_CAR','BETA_COST_SHARE_PT','BETA_DIST','BETA_LANGUAGE','BETA_NbCar','BETA_NbChild','BETA_Nbikes','BETA_Student','BETA_TIME_CAR','BETA_TIME_PT','BETA_Urban','BETA_WorkTrip','LAMBDA_DIST','LAMBDA_TIME_CAR','LAMBDA_TIME_PT']
#values = [[0.111381,0.0659011,-0.00972123,-0.000514929,0.00433747,-0.00253901,-0.0223268,-0.000656427,-7.79222e-05,-0.0203082,-0.000868916,0.0081118,0.00794477,-0.0012392,0.000361096,-0.00142455,0.0197838],[0.0659011,0.125042,-0.00371703,0.00128651,-0.00848617,0.000509732,-0.00416989,-0.00194345,-0.0125728,-0.00454859,0.00111624,0.00660976,0.00579063,0.00150068,-0.00092844,-0.000612172,0.0153859],[-0.00972123,-0.00371703,0.0345017,0.00854163,-0.00441407,-0.00279526,0.00373273,0.000650666,-0.000467504,-0.000423469,-0.00180059,-0.00267682,0.000523793,4.48698e-05,-0.00344091,-0.0010273,-0.00966841],[-0.000514929,0.00128651,0.00854163,0.00537295,-0.00124521,-0.000299962,0.00105173,-7.39668e-05,-0.000252842,-0.000977864,-0.000579437,-0.000458129,-0.000433571,-0.000767562,-0.00129248,-0.00107402,-0.0019071],[0.00433747,-0.00848617,-0.00441407,-0.00124521,0.0348557,-0.000592101,-0.000379517,-0.000561254,-0.00163592,-0.00322514,0.00805802,0.00327077,0.000853144,0.00184717,0.00887252,0.00452432,0.00728315],[-0.00253901,0.000509732,-0.00279526,-0.000299962,-0.000592101,0.030827,-0.000698604,-0.000501042,0.000198764,0.000188257,-1.66336e-06,1.03463e-05,0.00426905,-0.000387415,4.15536e-05,6.87328e-05,0.000416982],[-0.0223268,-0.00416989,0.00373273,0.00105173,-0.000379517,-0.000698604,0.0172257,-0.000421761,0.000630989,0.0146676,3.17746e-05,-0.000482536,-0.000868342,-0.00329529,-0.00024135,9.35544e-05,-0.0015007],[-0.000656427,-0.00194345,0.000650666,-7.39668e-05,-0.000561254,-0.000501042,-0.000421761,0.00523576,0.00127937,0.00219976,-0.000236627,-4.46445e-05,0.000488417,-0.000581983,-0.000191817,2.2337e-06,-0.000103057],[-7.79222e-05,-0.0125728,-0.000467504,-0.000252842,-0.00163592,0.000198764,0.000630989,0.00127937,0.00491815,0.00172347,-4.51895e-05,5.76366e-05,0.000360278,-0.000564229,-0.000490388,4.80059e-05,0.000198464],[-0.0203082,-0.00454859,-0.000423469,-0.000977864,-0.00322514,0.000188257,0.0146676,0.00219976,0.00172347,0.180778,-0.00227436,-0.00118174,-0.00415093,0.000198598,0.00153654,0.000100769,-0.0016735],[-0.000868916,0.00111624,-0.00180059,-0.000579437,0.00805802,-1.66336e-06,3.17746e-05,-0.000236627,-4.51895e-05,-0.00227436,0.00610803,0.00194604,-9.79765e-06,5.29523e-05,0.00101273,0.00358761,0.00418403],[0.0081118,0.00660976,-0.00267682,-0.000458129,0.00327077,1.03463e-05,-0.000482536,-4.46445e-05,5.76366e-05,-0.00118174,0.00194604,0.00169689,-0.000291869,0.000461801,0.000488551,0.00102516,0.00414343],[0.00794477,0.00579063,0.000523793,-0.000433571,0.000853144,0.00426905,-0.000868342,0.000488417,0.000360278,-0.00415093,-9.79765e-06,-0.000291869,0.019321,-0.00035637,0.000494034,0.000261777,-0.000619908],[-0.0012392,0.00150068,4.48698e-05,-0.000767562,0.00184717,-0.000387415,-0.00329529,-0.000581983,-0.000564229,0.000198598,5.29523e-05,0.000461801,-0.00035637,0.0178434,0.000660486,0.000367861,0.00126067],[0.000361096,-0.00092844,-0.00344091,-0.00129248,0.00887252,4.15536e-05,-0.00024135,-0.000191817,-0.000490388,0.00153654,0.00101273,0.000488551,0.000494034,0.000660486,0.00404962,0.00119895,0.00180613],[-0.00142455,-0.000612172,-0.0010273,-0.00107402,0.00452432,6.87328e-05,9.35544e-05,2.2337e-06,4.80059e-05,0.000100769,0.00358761,0.00102516,0.000261777,0.000367861,0.00119895,0.00343115,0.00302221],[0.0197838,0.0153859,-0.00966841,-0.0019071,0.00728315,0.000416982,-0.0015007,-0.000103057,0.000198464,-0.0016735,0.00418403,0.00414343,-0.000619908,0.00126067,0.00180613,0.00302221,0.0112266]]

#vc = bioMatrix(17,names,values)
#BIOGEME_OBJECT.VARCOVAR = vc