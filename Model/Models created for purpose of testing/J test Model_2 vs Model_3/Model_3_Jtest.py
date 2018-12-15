# Null hypothesis: The specification in Model_3 is correct

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS


ASC_SM = Beta('ASC_SM',-0.471445,-10000,10000,0,'ASC_SM' )

ASC_DIST = Beta('ASC_DIST',-9.77888,-10000,10000,0,'ASC_DIST' )

BETA_DIST_YOUNG = Beta('BETA_DIST_YOUNG',0.529798,-10000,10000,0,'BETA_DIST_YOUNG' )

BETA_DIST_ADULT = Beta('BETA_DIST_ADULT',0.00171794,-10000,10000,0,'BETA_DIST_ADULT' )

BETA_DIST_OLD = Beta('BETA_DIST_OLD',-0.030165,-10000,10000,0,'BETA_DIST_OLD' )

BETA_Nbikes = Beta('BETA_Nbikes',0.304771,-10000,10000,0,'BETA_Nbikes' )

BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',-0.316804,-10000,10000,0,'BETA_COST_SHARE_PT' )

BETA_TIME_PT = Beta('BETA_TIME_PT',-0.0109667,-10000,10000,0,'BETA_TIME_PT' )

BETA_Urban = Beta('BETA_Urban',0.192654,-10000,10000,0,'BETA_Urban' )

BETA_Student = Beta('BETA_Student',3.17509,-10000,10000,0,'BETA_Student' )

ASC_CAR = Beta('ASC_CAR',-0.819596,-10000,10000,0,'ASC_CAR' )

BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',-0.546384,-10000,10000,0,'BETA_COST_SHARE_CAR' )

BETA_TIME_CAR = Beta('BETA_TIME_CAR',-0.0212809,-10000,10000,0,'BETA_TIME_CAR' )

BETA_NbCar = Beta('BETA_NbCar',1.20775,-10000,10000,0,'BETA_NbCar' )

BETA_NbChild = Beta('BETA_NbChild',0.191268,-10000,10000,0,'BETA_NbChild' )

BETA_LANGUAGE = Beta('BETA_LANGUAGE',1.02732,-10000,10000,0,'BETA_LANGUAGE' )

BETA_WorkTrip = Beta('BETA_WorkTrip',-0.539565,-10000,10000,0,'BETA_WorkTrip' )

# Newest parameters

ALFA = Beta('ALFA',0,-10000,10000,0)


#Model 2 estimations
BETA_COST_PT_2 = Beta('BETA_COST_PT_2',-0.0581022,-10000,10000,1,'BETA_COST_PT_2' )
BETA_TIME_PT_2 = Beta('BETA_TIME_PT_2',-0.0111887,-10000,10000,1,'BETA_TIME_PT_2' )

BETA_Urban_2 = Beta('BETA_Urban_2',0.294817,-10000,10000,1,'BETA_Urban_2' )

BETA_Student_2 = Beta('BETA_Student_2',3.1116,-10000,10000,1,'BETA_Student_2' )

ASC_SM_2 = Beta('ASC_SM_2',-0.41921,-10000,10000,1,'ASC_SM_2' )

BETA_DIST_2 = Beta('BETA_DIST_2',-0.21187,-10000,10000,1,'BETA_DIST_2' )

BETA_Nbikes_2 = Beta('BETA_Nbikes_2',0.318486,-10000,10000,1,'BETA_Nbikes_2' )

ASC_CAR_2 = Beta('ASC_CAR_2',-0.405704,-10000,10000,1,'ASC_CAR_2' )

BETA_COST_CAR_2 = Beta('BETA_COST_CAR_2',-0.0395305,-10000,10000,1,'BETA_COST_CAR_2' )

BETA_TIME_CAR_2 = Beta('BETA_TIME_CAR_2',-0.0317558,-10000,10000,1,'BETA_TIME_CAR_2' )

BETA_NbCar_2 = Beta('BETA_NbCar_2',1.03013,-10000,10000,1,'BETA_NbCar_2' )

BETA_NbChild_2 = Beta('BETA_NbChild_2',0.142707,-10000,10000,1,'BETA_NbChild_2' )

BETA_LANGUAGE_2 = Beta('BETA_LANGUAGE_2',1.11214,-10000,10000,1,'BETA_LANGUAGE_2' )

BETA_WorkTrip_2 = Beta('BETA_WorkTrip_2',-0.552273,-10000,10000,1,'BETA_WorkTrip_2' )
# VARIABLES

one = DefineVariable('one',1)
FrenchRegion = DefineVariable('FrenchRegion', LangCode == 1 )
WORK = DefineVariable('WORK', ((TripPurpose == 1) + (TripPurpose == 2)) > 0 )
URBAN = DefineVariable('URBAN', UrbRur == 2 )
STUDENT = DefineVariable('STUDENT', OccupStat == 8 )
NbCars = DefineVariable('NbCars', NbCar * (NbCar > 0) )
NbBikes = DefineVariable('NbBikes', NbBicy * (NbBicy > 0) )
NbChildren = DefineVariable('NbChildren', NbChild * (NbChild > 0) )

# New variables 

Age = DefineVariable('Age', 2010 - BirthYear)
AgeYoung = DefineVariable('AgeYoung', (Age > 18) * 18 + Age * (Age <= 18))
AgeAdult = DefineVariable('AgeAdult', (Age > 65) * (65 - 18) + (Age - 18) * (18 < Age <= 65))
AgeOld = DefineVariable('AgeOld', (Age > 65) * (Age - 65))

# Cost shares are normalized to get a smaller beta value for car and PT

ApproxIncome = DefineVariable('ApproxIncome', (Income == -1) * 7000 + (Income == 1) * 2500 + (Income == 2) * 3250 + (Income==3) * 5000 + (Income == 4) * 7000 + (Income == 5) * 9000 + (Income == 6) * 10000)
CostCarShare_norm = DefineVariable('CostCarShare_norm', CostCarCHF * 1000/ApproxIncome)
CostPTShare_norm = DefineVariable('CostPTShare_norm', MarginalCostPT * 1000/ApproxIncome)



# UTILITIES

#For Model 3:
CAR_3 = ASC_CAR * one +\
 BETA_COST_SHARE_CAR * CostCarShare_norm +\
 BETA_TIME_CAR * TimeCar +\
 BETA_NbCar * NbCars +\
 BETA_NbChild * NbChildren +\
 BETA_LANGUAGE * FrenchRegion +\
 BETA_WorkTrip * WORK

PT_3 = BETA_COST_SHARE_PT * CostPTShare_norm +\
 BETA_TIME_PT * TimePT +\
 BETA_Urban * URBAN +\
 BETA_Student * STUDENT

SM_3 = ASC_SM * one +\
 (ASC_DIST + BETA_DIST_YOUNG * AgeYoung + BETA_DIST_ADULT * AgeAdult + BETA_DIST_OLD * AgeOld) * distance_km  +\
 BETA_Nbikes * NbBikes

#Model 2:

CAR_2 = ASC_CAR_2 * one +\
 BETA_COST_CAR_2 * CostCarCHF +\
 BETA_TIME_CAR_2 * TimeCar +\
 BETA_NbCar_2 * NbCars +\
 BETA_NbChild_2 * NbChildren +\
 BETA_LANGUAGE_2 * FrenchRegion +\
 BETA_WorkTrip_2 * WORK

PT_2 = BETA_COST_PT_2 * MarginalCostPT +\
 BETA_TIME_PT_2 * TimePT +\
 BETA_Urban_2 * URBAN +\
 BETA_Student_2 * STUDENT 

SM_2 = ASC_SM_2 * one +\
 BETA_DIST_2 * distance_km +\
 BETA_Nbikes_2 * NbBikes

CAR = (1.0 - ALFA) * CAR_3 + ALFA * CAR_2
PT = (1.0 - ALFA) * PT_3 + ALFA * PT_2
SM = (1.0 - ALFA) * SM_3 + ALFA * SM_2

#__V = {1: V1,2: V2,3: V3}

V = {1: CAR, 2: SM, 0: PT}

av = {1: one, 2: one, 0: one}

# EXCLUDE
BIOGEME_OBJECT.EXCLUDE = (Choice == -1) + (BirthYear == -1) + (Income == -1) # I exclude the respondents whose age we can not calculate or whose income we don't know
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
