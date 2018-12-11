########################################
# v532_optima_base
########################################
# v532_optima_base
# Atasoy et al., 2013
########################################


########## MODEL 1 #####################

# In this model, the parameters are set to be alternative specific. This concerns the time and cost parameters. 

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS

ASC_CAR = Beta('ASC_CAR',0,-10000,10000,0)
ASC_SM = Beta('ASC_SM',0,-10000,10000,0)
BETA_DIST = Beta('BETA_DIST',0,-10000,10000,0)

# New parameters

BETA_COST_CAR = Beta('BETA_COST_CAR',0,-10000,10000,0)
BETA_COST_PT = Beta('BETA_COST_PT',0,-10000,10000,0)
BETA_TIME_CAR = Beta('BETA_TIME_CAR',0,-10000,10000,0)
BETA_TIME_PT = Beta('BETA_TIME_PT',0,-10000,10000,0)



# VARIABLES

one = DefineVariable('one',1)



# UTILITIES

CAR = ASC_CAR + BETA_COST_CAR * CostCarCHF + BETA_TIME_CAR * TimeCar

PT = BETA_COST_PT * MarginalCostPT + BETA_TIME_PT * TimePT 

SM = ASC_SM + BETA_DIST * distance_km 

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}



# Exclude

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
