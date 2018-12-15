# Null hypothesis: The specification in Model_3 is correct

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *



# PARAMETERS (from Model_4_param)

ASC_CAR = Beta('ASC_CAR',-0.392432,-10000,10000,0,'ASC_CAR' )
BETA_COST_SHARE_CAR = Beta('BETA_COST_SHARE_CAR',-0.537653,-10000,10000,0,'BETA_COST_SHARE_CAR' )
BETA_TIME_CAR = Beta('BETA_TIME_CAR',-0.116882,-10000,10000,0,'BETA_TIME_CAR' )
LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',0.634672,-1000,1000,0,'LAMBDA_TIME_CAR' )
BETA_NbCar = Beta('BETA_NbCar',1.20729,-10000,10000,0,'BETA_NbCar' )
BETA_NbChild = Beta('BETA_NbChild',0.194942,-10000,10000,0,'BETA_NbChild' )
BETA_LANGUAGE = Beta('BETA_LANGUAGE',0.99994,-10000,10000,0,'BETA_LANGUAGE' )
BETA_WorkTrip = Beta('BETA_WorkTrip',-0.487827,-10000,10000,0,'BETA_WorkTrip' )
BETA_COST_SHARE_PT = Beta('BETA_COST_SHARE_PT',-0.282421,-10000,10000,0,'BETA_COST_SHARE_PT' )
BETA_TIME_PT = Beta('BETA_TIME_PT',-0.0171339,-10000,10000,0,'BETA_TIME_PT' )
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',0.950997,-1000,1000,0,'LAMBDA_TIME_PT' )
BETA_Urban = Beta('BETA_Urban',0.222714,-10000,10000,0,'BETA_Urban' )
BETA_Student = Beta('BETA_Student',3.28702,-10000,10000,0,'BETA_Student' )
ASC_SM = Beta('ASC_SM',-0.214546,-10000,10000,0,'ASC_SM' )
ASC_DIST = Beta('ASC_DIST',-10.0599,-10000,10000,0,'ASC_DIST' )
BETA_DIST_YOUNG = Beta('BETA_DIST_YOUNG',0.543686,-10000,10000,0,'BETA_DIST_YOUNG' )
BETA_DIST_ADULT = Beta('BETA_DIST_ADULT',0.00173394,-10000,10000,0,'BETA_DIST_ADULT' )
BETA_DIST_OLD = Beta('BETA_DIST_OLD',-0.0314759,-10000,10000,0,'BETA_DIST_OLD' )
BETA_Nbikes = Beta('BETA_Nbikes',0.305972,-10000,10000,0,'BETA_Nbikes' )

# Newest parameters

ALFA = Beta('ALFA',0,-10000,10000,0)

# New parameters

LAMBDA_TIME_CAR = Beta('LAMBDA_TIME_CAR',1,-1000,1000,0)
LAMBDA_TIME_PT = Beta('LAMBDA_TIME_PT',1,-1000,1000,0)

# Model 3 estimations:
ASC_CAR_4 = Beta('ASC_CAR_4',-0.392432,-10000,10000,1 )
BETA_COST_SHARE_CAR_4 = Beta('BETA_COST_SHARE_CAR_4',-0.537653,-10000,10000,1 )
BETA_TIME_CAR_4 = Beta('BETA_TIME_CAR_4',-0.116882,-10000,10000,1 )
LAMBDA_TIME_CAR_4 = Beta('LAMBDA_TIME_CAR_4',0.634672,-1000,1000,1)
BETA_NbCar_4 = Beta('BETA_NbCar_4',1.20729,-10000,10000,1)
BETA_NbChild_4 = Beta('BETA_NbChild_4',0.194942,-10000,10000,1)
BETA_LANGUAGE_4 = Beta('BETA_LANGUAGE_4',0.99994,-10000,10000,1)
BETA_WorkTrip_4 = Beta('BETA_WorkTrip_4',-0.487827,-10000,10000,1)
BETA_COST_SHARE_PT_4 = Beta('BETA_COST_SHARE_PT_4',-0.282421,-10000,10000,1 )
BETA_TIME_PT_4 = Beta('BETA_TIME_PT_4',-0.0171339,-10000,10000,1)
LAMBDA_TIME_PT_4 = Beta('LAMBDA_TIME_PT_4',0.950997,-1000,1000,1)
BETA_Urban_4 = Beta('BETA_Urban_4',0.222714,-10000,10000,1)
BETA_Student_4 = Beta('BETA_Student_4',3.28702,-10000,10000,1)
ASC_SM_4 = Beta('ASC_SM_4',-0.214546,-10000,10000,1)
ASC_DIST_4 = Beta('ASC_DIST_4',-10.0599,-10000,10000,1)
BETA_DIST_YOUNG_4 = Beta('BETA_DIST_YOUNG_4',0.543686,-10000,10000,1)
BETA_DIST_ADULT_4 = Beta('BETA_DIST_ADULT_4',0.00173394,-10000,10000,1)
BETA_DIST_OLD_4 = Beta('BETA_DIST_OLD_4',-0.0314759,-10000,10000,1)
BETA_Nbikes_4 = Beta('BETA_Nbikes_4',0.305972,-10000,10000,1)

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

#For Model_3:

CAR_3 = ASC_CAR * one +\
 BETA_COST_SHARE_CAR * CostCarShare_norm +\
 BETA_TIME_CAR * ((TimeCar ** LAMBDA_TIME_CAR) - 1)/LAMBDA_TIME_CAR +\
 BETA_NbCar * NbCars +\
 BETA_NbChild * NbChildren +\
 BETA_LANGUAGE * FrenchRegion +\
 BETA_WorkTrip * WORK

PT_3 = BETA_COST_SHARE_PT * CostPTShare_norm +\
 BETA_TIME_PT * ((TimePT ** LAMBDA_TIME_PT) - 1)/LAMBDA_TIME_PT +\
 BETA_Urban * URBAN +\
 BETA_Student * STUDENT

SM_3 = ASC_SM * one +\
 (ASC_DIST + BETA_DIST_YOUNG * AgeYoung + BETA_DIST_ADULT * AgeAdult + BETA_DIST_OLD * AgeOld) * distance_km  +\
 BETA_Nbikes * NbBikes
 
#For Model_4:
CAR_4 = ASC_CAR_4 * one +\
 BETA_COST_SHARE_CAR_4 * CostCarShare_norm +\
 BETA_TIME_CAR_4 * TimeCar +\
 BETA_NbCar_4 * NbCars +\
 BETA_NbChild_4 * NbChildren +\
 BETA_LANGUAGE_4 * FrenchRegion +\
 BETA_WorkTrip_4 * WORK

PT_4 = BETA_COST_SHARE_PT_4 * CostPTShare_norm +\
 BETA_TIME_PT_4 * TimePT +\
 BETA_Urban_4 * URBAN +\
 BETA_Student_4 * STUDENT

SM_4 = ASC_SM_4 * one +\
 (ASC_DIST_4 + BETA_DIST_YOUNG_4 * AgeYoung + BETA_DIST_ADULT_4 * AgeAdult + BETA_DIST_OLD_4 * AgeOld) * distance_km  +\
 BETA_Nbikes_4 * NbBikes

CAR = (1.0 - ALFA) * CAR_3 + ALFA * CAR_4
PT = (1.0 - ALFA) * PT_3 + ALFA * PT_4
SM = (1.0 - ALFA) * SM_3 + ALFA * SM_4
 
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

