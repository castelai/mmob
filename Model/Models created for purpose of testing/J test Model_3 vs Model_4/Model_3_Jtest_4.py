# Null hypothesis: The specification in Model_4 is correct
#So here we put estimated parameters in Model_3, parameters for Model_4 we calculate

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

# New parameters

LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',1,-1000,1000,0)
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',1,-1000,1000,0)

# Model 3 estimations:
ASC_SM_3 = Beta('ASC_SM_3',-0.471445,-10000,10000,1)
ASC_DIST_3 = Beta('ASC_DIST_3',-9.77888,-10000,10000,1)
BETA_DIST_YOUNG_3 = Beta('BETA_DIST_YOUNG_3',0.529798,-10000,10000,1)
BETA_DIST_ADULT_3 = Beta('BETA_DIST_ADULT_3',0.00171794,-10000,10000,1 )
BETA_DIST_OLD_3 = Beta('BETA_DIST_OLD_3',-0.030165,-10000,10000,1)
BETA_Nbikes_3 = Beta('BETA_Nbikes_3',0.304771,-10000,10000,1)
BETA_COST_SHARE_PT_3 = Beta('BETA_COST_SHARE_PT_3',-0.316804,-10000,10000,1)
BETA_TIME_PT_3 = Beta('BETA_TIME_PT_3',-0.0109667,-10000,10000,1)
BETA_Urban_3 = Beta('BETA_Urban_3',0.192654,-10000,10000,1)
BETA_Student_3 = Beta('BETA_Student_3',3.17509,-10000,10000,1 )
ASC_CAR_3 = Beta('ASC_CAR_3',-0.819596,-10000,10000,1)
BETA_COST_SHARE_CAR_3 = Beta('BETA_COST_SHARE_CAR_3',-0.546384,-10000,10000,1)
BETA_TIME_CAR_3 = Beta('BETA_TIME_CAR_3',-0.0212809,-10000,10000,1)
BETA_NbCar_3 = Beta('BETA_NbCar_3',1.20775,-10000,10000,1)
BETA_NbChild_3 = Beta('BETA_NbChild_3',0.191268,-10000,10000,1)
BETA_LANGUAGE_3 = Beta('BETA_LANGUAGE_3',1.02732,-10000,10000,1)
BETA_WorkTrip_3 = Beta('BETA_WorkTrip_3',-0.539565,-10000,10000,1)

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
CostCarShare_norm = DefineVariable('CostCarShare_norm', CostCarCHF * 1000/ApproxIncome)
CostPTShare_norm = DefineVariable('CostPTShare_norm', MarginalCostPT * 1000/ApproxIncome)



# UTILITIES

#For Model_4:

CAR_4 = ASC_CAR * one +\
 BETA_COST_SHARE_CAR * CostCarShare_norm +\
 BETA_TIME_CAR * ((TimeCar ** LAMBDA_TIME_CAR) - 1)/LAMBDA_TIME_CAR +\
 BETA_NbCar * NbCars +\
 BETA_NbChild * NbChildren +\
 BETA_LANGUAGE * FrenchRegion +\
 BETA_WorkTrip * WORK

PT_4 = BETA_COST_SHARE_PT * CostPTShare_norm +\
 BETA_TIME_PT * ((TimePT ** LAMBDA_TIME_PT) - 1)/LAMBDA_TIME_PT +\
 BETA_Urban * URBAN +\
 BETA_Student * STUDENT

SM_4 = ASC_SM * one +\
 (ASC_DIST + BETA_DIST_YOUNG * AgeYoung + BETA_DIST_ADULT * AgeAdult + BETA_DIST_OLD * AgeOld) * distance_km  +\
 BETA_Nbikes * NbBikes
 
#For Model_3:
CAR_3 = ASC_CAR_3 * one +\
 BETA_COST_SHARE_CAR_3 * CostCarShare_norm +\
 BETA_TIME_CAR_3 * TimeCar +\
 BETA_NbCar_3 * NbCars +\
 BETA_NbChild_3 * NbChildren +\
 BETA_LANGUAGE_3 * FrenchRegion +\
 BETA_WorkTrip_3 * WORK

PT_3 = BETA_COST_SHARE_PT_3 * CostPTShare_norm +\
 BETA_TIME_PT_3 * TimePT +\
 BETA_Urban_3 * URBAN +\
 BETA_Student_3 * STUDENT

SM_3 = ASC_SM_3 * one +\
 (ASC_DIST_3 + BETA_DIST_YOUNG_3 * AgeYoung + BETA_DIST_ADULT_3 * AgeAdult + BETA_DIST_OLD_3 * AgeOld) * distance_km  +\
 BETA_Nbikes_3 * NbBikes

CAR = (1.0 - ALFA) * CAR_4 + ALFA * CAR_3
PT = (1.0 - ALFA) * PT_4 + ALFA * PT_3
SM = (1.0 - ALFA) * SM_4 + ALFA * SM_3
 
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

