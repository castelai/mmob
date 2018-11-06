# File firstmodel.py
# Author : Michel Bierlaire
# Example of a simple model to be estimated with Biogeme

from biogeme import * 
from headers import *

#PT: Public Transport
#Private: Cars
#Soft: Walking, cycling

ASC_PRIVATE = Beta('ASC_PRIVATE',0,-1000,1000,0)
ASC_PT = Beta('ASC_PT',0,-1000,1000,0)
ASC_SOFT = Beta('ASC_SOFT',0,-1000,1000,0)
B_TIME = Beta('B_TIME',0,-1000,1000,0)
B_COST = Beta('B_COST',0,-1000,1000,0)

# Definition of additional variables
TimeBK = DefineVariable('TimeBK', (distance_km/16)*60) #Bicycle travel time (averaging on a 16km/h speed)
CAR_AV = DefineVariable('CAR_AV', (CarAvail != 3)*(CarAvail != -1))
BIKE_AV = DefineVariable('BIKE_AV', (NbBicy != -1)*(NbBicy != 0))

# Definition of the utility functions 
V0 = ASC_PT + \
	 B_TIME * TimePT + \
	 B_COST * (CostPT + MarginalCostPT * (1- max(0.5*(HalfFareST == 1),(LineRelST == 1),(GenAbST == 1),(AreaRelST == 1),(OtherST == 1))))

V1 = ASC_PRIVATE + \
	 B_TIME * TimeCar + \
	 B_COST * CostCarCHF

V2 = ASC_SOFT + \
	 B_TIME * TimeBK 

# Associate the utility function swith the numbering of the alternatives

V = {0: V0, 
	 1: V1,
	 2: V2}

# Availability of each alternative , as described in the data set

av = {0: 1,
	  1: CAR_AV,
	  2: BIKE_AV}

# The choice model is a logit, with availability conditions
logprob = bioLogLogit(V,av,CHOICE)

# Defines an interator on the data
rowIterator('obsIter')

# Define the log likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(logprob,'obsIter')

# We remove observations such that the CHOICE variable is equal to 0
exclude = (CHOICE == -1)

BIOGEME_OBJECT.EXCLUDE = exclude
