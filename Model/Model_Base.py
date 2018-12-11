########################################
# v532_optima_base
# Atasoy et al., 2013
########################################

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_CAR = Beta('ASC_CAR',0,-10000,10000,0)
ASC_SM = Beta('ASC_SM',0,-10000,10000,0)
BETA_COST = Beta('BETA_COST',0,-10000,10000,0)
BETA_TIME = Beta('BETA_TIME',0,-10000,10000,0)
#BETA_TIME_PT = Beta('BETA_TIME_PT',0,-10000,10000,0)
BETA_DIST = Beta('BETA_DIST',0,-10000,10000,0)
#BETA_NbCar = Beta('BETA_NbCar',0,-10000,10000,0)
#BETA_NbChild = Beta('BETA_NbChild',0,-10000,10000,0)
#BETA_LANGUAGE = Beta('BETA_LANGUAGE',0,-10000,10000,0)
#BETA_WorkTrip = Beta('BETA_WorkTrip',0,-10000,10000,0)
#BETA_Urban = Beta('BETA_Urban',0,-10000,10000,0)
#BETA_Student = Beta('BETA_Student',0,-10000,10000,0)
#BETA_Nbikes = Beta('BETA_Nbikes',0,-10000,10000,0)


# Define here arithmetic expressions for name that are not directly 
# available from the data

one = DefineVariable('one',1)
#FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
#WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
#URBAN = DefineVariable('URBAN', UrbRur == 2 )
#STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
#NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
#NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
#NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

#Utilities
CAR = ASC_CAR * one + BETA_COST * CostCarCHF + BETA_TIME * TimeCar #+ BETA_NbCar * NbCars + BETA_NbChild * NbChildren + BETA_LANGUAGE * FrenchRegion + BETA_WorkTrip * WORK

PT = BETA_COST * MarginalCostPT + BETA_TIME * TimePT #+ BETA_Urban * URBAN + BETA_Student * STUDENT

SM = ASC_SM * one + BETA_DIST * distance_km #+ BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}
av = {1: one, 2: one, 0: one}

#Exclude
BIOGEME_OBJECT.EXCLUDE = (Choice == -1)

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
