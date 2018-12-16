# This file has automatically been generated
# biogeme 2.6a [Wed, Apr 19, 2017 7:57:38 AM]
# <a href='http://people.epfl.ch/michel.bierlaire'>Michel Bierlaire</a>, <a href='http://transp-or.epfl.ch'>Transport and Mobility Laboratory</a>, <a href='http://www.epfl.ch'>Ecole Polytechnique F&eacute;d&eacute;rale de Lausanne (EPFL)</a>
# 12/13/18 16:41:55</p>
#
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


## Code for the sensitivity analysis
names = ['ASC_CAR','ASC_DIST','ASC_SM','BETA_COST_SHARE_CAR','BETA_COST_SHARE_PT','BETA_DIST_ADULT','BETA_DIST_OLD','BETA_DIST_YOUNG','BETA_LANGUAGE','BETA_NbCar','BETA_NbChild','BETA_Nbikes','BETA_Student','BETA_TIME_CAR','BETA_TIME_PT','BETA_Urban','BETA_WorkTrip']
values = [[0.044844,-0.0151216,0.00621869,0.0035475,0.00236323,-4.44987e-006,7.86262e-005,0.000945858,-0.00113935,-0.0186578,-0.001261,-0.00018441,-0.0178696,0.000216755,0.000174748,0.00947682,-0.00531122],[-0.0151216,7.64995,0.0228762,0.0213525,0.0023579,0.00257759,-0.00628356,-0.429295,0.0124607,0.0382308,-0.0130524,-0.0106203,0.332584,0.00159345,0.00102709,0.00353234,0.00351841],[0.00621869,0.0228761,0.154224,0.00887632,0.00294211,-0.00011336,-0.000125854,-0.00186289,0.00140659,0.00290036,-0.000831182,-0.0128378,0.00723622,-9.57769e-005,1.57362e-005,0.00750807,-0.0038597],[0.0035475,0.0213525,0.00887632,0.0398953,0.00869759,1.98626e-006,6.76978e-006,-0.00112378,-0.00184466,0.00479174,0.000994179,-0.000211367,-0.00249559,-0.000138094,0.000248559,0.00108367,0.000587586],[0.00236323,0.0023579,0.00294211,0.00869759,0.00704646,8.90887e-007,3.95355e-006,-8.99578e-005,-0.000300072,0.00107385,-0.000192244,-0.000301391,-0.00200477,0.000197205,8.89166e-005,-0.000366281,-0.00104394],[-4.44987e-006,0.00257759,-0.00011336,1.98626e-006,8.90887e-007,4.96263e-006,-1.18485e-005,-0.000151562,-2.90961e-005,2.55769e-005,-3.1729e-005,2.8896e-005,0.000179249,1.05171e-006,5.94554e-007,-2.49075e-005,-5.25762e-006],[7.86262e-005,-0.00628356,-0.000125854,6.76978e-006,3.95355e-006,-1.18485e-005,0.000149858,0.0003678,0.000205267,-6.60452e-005,4.88133e-005,3.94178e-005,-0.000417473,-3.28052e-006,-1.61944e-006,7.584e-005,-4.94637e-005],[0.000945857,-0.429297,-0.0018629,-0.00112378,-8.99579e-005,-0.000151562,0.0003678,0.0241106,-0.000650554,-0.00219171,0.000773765,0.000537487,-0.0189468,-8.50802e-005,-5.53058e-005,-0.00014928,-0.000158436],[-0.00113935,0.0124607,0.00140659,-0.00184466,-0.000300072,-2.90961e-005,0.000205267,-0.000650554,0.0310478,-0.00110995,-0.000719561,-0.000102045,0.00083105,-7.92949e-006,-2.29796e-005,0.00547077,-0.000832778],[-0.0186578,0.0382308,0.00290036,0.00479174,0.00107385,2.55769e-005,-6.60452e-005,-0.00219171,-0.00110995,0.016824,-0.000639414,0.000286398,0.013384,-3.40746e-005,1.57322e-005,-0.00072182,-0.0030034],[-0.001261,-0.0130524,-0.000831182,0.000994179,-0.000192244,-3.1729e-005,4.88133e-005,0.000773765,-0.000719561,-0.000639414,0.00522113,0.000937766,0.00143934,-2.97675e-005,3.28788e-007,0.000430323,-6.83294e-005],[-0.00018441,-0.0106203,-0.0128378,-0.000211367,-0.000301391,2.8896e-005,3.94178e-005,0.000537486,-0.000102045,0.000286398,0.000937766,0.00429848,0.00241066,-4.62338e-006,1.38005e-006,0.000253181,-0.000418251],[-0.0178696,0.332584,0.00723622,-0.00249559,-0.00200477,0.000179249,-0.000417473,-0.0189468,0.00083105,0.013384,0.00143934,0.00241066,0.160057,-0.000139118,-8.09723e-005,-0.00377272,-0.000630927],[0.000216755,0.00159345,-9.57769e-005,-0.000138094,0.000197205,1.05171e-006,-3.28052e-006,-8.50802e-005,-7.92949e-006,-3.40746e-005,-2.97675e-005,-4.62338e-006,-0.000139118,3.63164e-005,1.18092e-005,-1.94482e-005,-6.83688e-005],[0.000174748,0.00102709,1.57362e-005,0.000248559,8.89166e-005,5.94554e-007,-1.61944e-006,-5.53058e-005,-2.29796e-005,1.57322e-005,3.28788e-007,1.38005e-006,-8.09723e-005,1.18092e-005,7.31597e-006,9.84401e-007,-9.03095e-006],[0.00947682,0.00353234,0.00750807,0.00108367,-0.000366281,-2.49075e-005,7.584e-005,-0.000149279,0.00547077,-0.00072182,0.000430323,0.000253181,-0.00377272,-1.94482e-005,9.84401e-007,0.0184881,-0.00104484],[-0.00531122,0.00351841,-0.0038597,0.000587586,-0.00104394,-5.25762e-006,-4.94637e-005,-0.000158436,-0.000832778,-0.0030034,-6.83294e-005,-0.000418251,-0.000630927,-6.83688e-005,-9.03095e-006,-0.00104484,0.01707]]
vc = bioMatrix(17,names,values)
BIOGEME_OBJECT.VARCOVAR = vc