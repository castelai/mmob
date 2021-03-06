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

ASC_CAR = Beta('ASC_CAR',0,-10000,10000,0)
ASC_SM = Beta('ASC_SM',0,-10000,10000,0)
BETA_TIME_CAR = Beta('BETA_TIME_CAR',0,-10000,10000,0)
BETA_TIME_PT = Beta('BETA_TIME_PT',0,-10000,10000,0)
BETA_NbCar = Beta('BETA_NbCar',0,-10000,10000,0)
BETA_NbChild = Beta('BETA_NbChild',0,-10000,10000,0)
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0,-10000,10000,0)
BETA_WorkTrip = Beta('BETA_WorkTrip',0,-10000,10000,0)
BETA_Urban = Beta('BETA_Urban',0,-10000,10000,0)
BETA_Student = Beta('BETA_Student',0,-10000,10000,0)
BETA_Nbikes = Beta('BETA_Nbikes',0,-10000,10000,0)
BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',0,-10000,10000,0)
BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',0,-10000,10000,0)
BETA_DIST = Beta('BETA_DIST',0,-10000,10000,0)
#BETA_DIST_YOUNG = Beta('BETA_DIST_YOUNG',0,-10000,10000,0) 
#BETA_DIST_ADULT = Beta('BETA_DIST_ADULT',0,-10000,10000,0) 
#BETA_DIST_OLD = Beta('BETA_DIST_OLD',0,-10000,10000,0)

# New parameters

LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',1,-1000,1000,0)
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',1,-1000,1000,0)
LAMBDA_DIST = Beta('LAMBDA_DIST',1,-1000,1000,0)


# VARIABLES

one = DefineVariable('one',1)
FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

#Age = DefineVariable('Age', 2010 - BirthYear)
#AgeYoung = DefineVariable('AgeYoung', (Age > 18) * 18 + Age * (Age <= 18))
#AgeAdult = DefineVariable('AgeAdult', (Age > 65) * (65 - 18) + (Age - 18) * (18 < Age <= 65))
#AgeOld = DefineVariable('AgeOld', (Age > 65) * (Age - 65))

ApproxIncome = DefineVariable('ApproxIncome', (Income == -1) * 7000 + (Income == 1) * 2500 + (Income == 2) * 3250 + (Income==3) * 5000 + (Income == 4) * 7000 + (Income == 5) * 9000 + (Income == 6) * 10000)
CostCarShare_norm = DefineVariable('CostCarShare_norm', CostCarCHF * 1000/ApproxIncome)
CostPTShare_norm = DefineVariable('CostPTShare_norm', MarginalCostPT * 1000/ApproxIncome)



# UTILITIES

CAR = ASC_CAR * one + BETA_COST_SHARE_CAR * CostCarShare_norm + BETA_TIME_CAR * ((TimeCar ** LAMBDA_TIME_CAR) - 1)/LAMBDA_TIME_CAR + BETA_NbCar * NbCars + BETA_NbChild * NbChildren + BETA_LANGUAGE * FrenchRegion + BETA_WorkTrip * WORK

PT = BETA_COST_SHARE_PT * CostPTShare_norm + BETA_TIME_PT * ((TimePT ** LAMBDA_TIME_PT) - 1)/LAMBDA_TIME_PT + BETA_Urban * URBAN + BETA_Student * STUDENT

SM = ASC_SM * one + BETA_DIST * ((distance_km**LAMBDA_DIST)-1)/LAMBDA_DIST  + BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}



# EXCLUDE

BIOGEME_OBJECT.EXCLUDE = (Choice == -1) + (Income == -1) # I exclude the respondents whose age we can not calculate or whose income we don't know

# MNL (Multinomial Logit model), with availability conditions
logprob = bioLogLogit(V,av,Choice)

# Defines an itertor on the data
rowIterator('obsIter')

# Define the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(logprob,'obsIter')

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
BIOGEME_OBJECT.STATISTICS['Sum of weights'] = Sum(Weight, 'obsIter')
