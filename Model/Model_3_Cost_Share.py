########################################
# v532_optima_base
# Atasoy et al., 2013
########################################

###### MODEL 3 COST SHARE ##############

# Here we use as a basis the Model_2, instead of the Model_2_augmented. We are going to include an interaction between the socioeconomic variables and the attributes. 
# In this program, we add an interaction with the revenue. The hypothesis is that the sensitivity to cost depends on the monthly revenue of the person. 
# Therefore, instead of looking at the absolute cost of the car or the public transport, we will instead look at the fraction of cost it represents. 
# An approximation to the actual income will be computed from the Income parameter that provides the income bracket to which the subject belongs.

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS

ASC_CAR = Beta('ASC_CAR',0,-10000,10000,0)
ASC_SM = Beta('ASC_SM',0,-10000,10000,0)
BETA_TIME_CAR = Beta('BETA_TIME_CAR',0,-10000,10000,0)
BETA_TIME_PT = Beta('BETA_TIME_PT',0,-10000,10000,0)
BETA_DIST = Beta('BETA_DIST',0,-10000,10000,0)
BETA_NbCar = Beta('BETA_NbCar',0,-10000,10000,0)
BETA_NbChild = Beta('BETA_NbChild',0,-10000,10000,0)
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0,-10000,10000,0)
BETA_WorkTrip = Beta('BETA_WorkTrip',0,-10000,10000,0)
BETA_Urban = Beta('BETA_Urban',0,-10000,10000,0)
BETA_Student = Beta('BETA_Student',0,-10000,10000,0)
BETA_Nbikes = Beta('BETA_Nbikes',0,-10000,10000,0)

# New parameters

BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',0,-10000,10000,0)
BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',0,-10000,10000,0)



# VARIABLES

one = DefineVariable('one',1)
FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

# Added variables : Income = -1 are excluded from the data (see excluded objects) even if approx income is computed with the mean income
# Cost shares are normalized to get a smaller beta value for car and PT

ApproxIncome = DefineVariable('ApproxIncome', (Income == -1) * 7000 + (Income == 1) * 2500 + (Income == 2) * 3250 + (Income==3) * 5000 + (Income == 4) * 7000 + (Income == 5) * 9000 + (Income == 6) * 10000)
CostCarShare_norm = DefineVariable('CostCarShare_norm', CostCarCHF * 1000/ApproxIncome)
CostPTShare_norm = DefineVariable('CostPTShare_norm', MarginalCostPT * 1000/ApproxIncome)


# UTILITIES

CAR = ASC_CAR * one + BETA_COST_SHARE_CAR * CostCarShare_norm + BETA_TIME_CAR * TimeCar + BETA_NbCar * NbCars + BETA_NbChild * NbChildren + BETA_LANGUAGE * FrenchRegion + BETA_WorkTrip * WORK

PT = BETA_COST_SHARE_PT * CostPTShare_norm + BETA_TIME_PT * TimePT + BETA_Urban * URBAN + BETA_Student * STUDENT

SM = ASC_SM * one + BETA_DIST * distance_km  + BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}

# EXCLUDE

BIOGEME_OBJECT.EXCLUDE = (Choice == -1) + (Income == -1) # I exclude the respondents whose income we do not know

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
