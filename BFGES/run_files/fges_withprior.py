
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from numpy import inf
import os 
import glob
import time
from functions import * 
import re 


hybrid_data = np.load("Dataset_main/13_sample_1000synthetic_dti_fmri_164.npy")
dti_data = np.load("DTI_priors/13_Prior_1000_fges_164.npy")
dtibar_data = np.load("DTI_priors/Not_10_Prior_164.npy")


numrun =10
dim = 125
name = '9_sample_synthetic_dti_fmri_125subP2_bayes_'

numsub = 5


for pen in [1,2,3,4,5,6,7,8,9,10]:
    print("pen:\n")
    print(pen)

    cnty = read_Cmrtx( name , pen , numsub ,10)
    cnty_withdir = read_Cmrtx( name + '_nonsym' , pen , numsub , 10)

    lastnum , restrun = assign_lambda(cnty)
    print(lastnum)
    print(restrun)

    for i3 , k in restrun:
        print(k)
        print(i3)

            
        np.savetxt('foo.csv' , dti_data[:,: , i3] , delimiter= ',')
        np.savetxt('notfoo.csv',dtibar_data[:,: , i3], delimiter= ',')
        
        
        from src.pycausal.pycausal import pycausal as pc
        from src.pycausal import prior as p
        from src.pycausal import search as s

        pc = pc()
        pc.start_vm()
        tetrad = s.tetradrunner()
        tetrad.getAlgorithmParameters(algoId = 'fges', scoreId = 'sem-bic-score')


        tetrad.run(algoId = 'fges', dfs = pd.DataFrame(hybrid_data[100:1200,:,i3]), scoreId = 'sem-bic-score',
                    maxDegree = -1 , faithfulnessAssumed = True, symmetricFirstStep = True,
                    penaltyDiscount = pen,
                    numberResampling = 5 , resamplingEnsemble = 2, addOriginalDataset = False ,
                    verbose = False)
        


        edges = tetrad.getEdges()

        num_int = []
        numb_ = []
        for line in edges :
            inp_str = line
            num = re.findall(r'\d+', inp_str) 
            numb_.append([int(i) for i in num][0:2])

        conn_mrx = np.zeros((dim, dim))
        conn_mrx_withdir = np.zeros((dim, dim))
        for i,j in numb_ :       
            if i==j :
                i=0            
            conn_mrx[i][j] = 1
            conn_mrx[j][i] = 1
            conn_mrx_withdir[i][j] = 1

        cnty[:,:,i3 ,k]= conn_mrx
        
        cnty_withdir[:,:,i3 ,k] = conn_mrx_withdir

        
        name1 = 'Data/' + 'connectivity_' + str(name) + '_' + str(pen)
        name2 =  'Data/' + 'connectivity_' + str(name)+ '_nonsym' + '_' + str(pen) 

       
        np.save(name1 ,cnty)
        np.save(name2 , cnty_withdir)








