
import tensorflow as tf
import pandas as pd 
import numpy as np
import os 
from tqdm.auto import tqdm , trange

import os
from models import GolemModel
from trainers import GolemTrainer
from functions import read_Cmrtx
from functions import * 

import logging
from utils.train import postprocess
from utils.utils import count_accuracy, set_seed
from golem_process import golm_process



data_path = "Dataset/"

dim = 164

dataset_names = ['13_sample_1000synthetic_dti_fmri_164']
 
expl = 'sub30_bayses'

for name in dataset_names :

  data = np.load(data_path + name + '.npy')
  print(data.shape)
  dataseri = 0.01
  numsub = 30
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  os.environ['CUDA_VISIBLE-DEVICES'] = '0'

 
  l1 = [j * 0.0001 for j in range(1,10)]
  l2 = [j * 0.001 for j in range(1,10)]
  l3 = [j * 0.01 for j in range(1,10)]
  l4 = [j * 0.1 for j in range(1,10)]
  #l5 = [j * 1 for j in range(1,10)]
  
  l0 = [0.001 , 0.003 , 0.005 , 0.007 , 0.009]
  l1 = [0.01 , 0.03 , 0.05 , 0.07 , 0.09]
  l2 = [0.1 , 0.3 , 0.5 , 0.7 , 0.9]

  #Lambda_list = l0 + l1 + l2 
  Lambda_list = [0.01]

  print(len(Lambda_list))

  cnty_w = read_Cmrtx( name , dataseri , numsub , len(Lambda_list))

  lastnum , lastlam = assign_lambda(cnty_w)
  print(lastnum)
  print(lastlam)



  for l in range(lastlam , len(Lambda_list)):

    lb = Lambda_list[l]
    
    print(lb)

    for i3 in trange(0,numsub):

      print('num_sub: ' + str(i3) + '\n')

      logging.basicConfig(
          level=logging.INFO,
          format='%(asctime)s %(levelname)s - %(name)s - %(message)s'
      )

      
      dataset = data[0:,: ,i3]

      set_seed(1)
      # GOLEM-EV
      B_est = golem(dataset, i3, lambda_1= lb , lambda_2=0.001,
                    equal_variances=True, checkpoint_iter=5000)
      

      cnty_w[:,:,i3,l]= B_est

      name2_mrtx = 'Golem_weights_' + name + '_' + str(dataseri) + expl
      np.save('Results/' + name2_mrtx ,cnty_w)

  golm_process(name2_mrtx)      



