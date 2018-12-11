########################################
# v532_optima_base
# Atasoy et al., 2013
########################################

######## MODEL 2 #######################

# This model is based on the research paper by Bilge Atasoy (https://www.tandfonline.com/doi/abs/10.1080/02513625.2013.827518). 
# The model parameters are kept and completed in the model 2 augmented. In this model, some attributes of the alternatives are added, as
# well as socioeconomic characteristics, to the utilities.

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS

ASC_CAR = Beta('ASC_CAR',0,-10000,10000,0)
ASC_SM = Beta('ASC_SM',0,-10000,10000,0)
BETA_COST_CAR = Beta('BETA_COST_CAR',0,-10000,10000,0)
BETA_COST_PT = Beta('BETA_COST_PT',0,-10000,10000,0)
BETA_TIME_CAR = Beta('BETA_TIME_CAR',0,-10000,10000,0)
BETA_TIME_PT = Beta('BETA_TIME_PT',0,-10000,10000,0)
BETA_DIST = Beta('BETA_DIST',0,-10000,10000,0)

# New parameters

BETA_NbCar = Beta('BETA_NbCar',0,-10000,10000,0)
BETA_NbChild = Beta('BETA_NbChild',0,-10000,10000,0)
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0,-10000,10000,0)
BETA_WorkTrip = Beta('BETA_WorkTrip',0,-10000,10000,0)
BETA_Urban = Beta('BETA_Urban',0,-10000,10000,0)
BETA_Student = Beta('BETA_Student',0,-10000,10000,0)
BETA_Nbikes = Beta('BETA_Nbikes',0,-10000,10000,0)



# VARIABLES

one = DefineVariable('one',1)

# New variables 

FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )



# UTILITIES

CAR = ASC_CAR * one + BETA_COST_CAR * CostCarCHF + BETA_TIME_CAR * TimeCar + BETA_NbCar * NbCars + BETA_NbChild * NbChildren + BETA_LANGUAGE * FrenchRegion + BETA_WorkTrip * WORK

PT = BETA_COST_PT * MarginalCostPT + BETA_TIME_PT * TimePT + BETA_Urban * URBAN + BETA_Student * STUDENT 

SM = ASC_SM * one + BETA_DIST * distance_km + BETA_Nbikes * NbBikes

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}

# EXCLUDE

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
