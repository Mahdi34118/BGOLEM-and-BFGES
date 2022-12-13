
import tensorflow as tf
import pandas as pd 
import numpy as np
import os 
from tqdm.auto import tqdm , trange

import os
from models import GolemModel
from trainers import GolemTrainer

import logging
from utils.train import postprocess
from utils.utils import count_accuracy, set_seed




def read_Cmrtx(name , la ,numsub , count_lamb) :



	dim = 164
	
	

	try :

	    name1 = os.getcwd() + '/Results/Golem_weights_' + name + '_' + str(la) + '.npy'
	    cnty_w = np.load(name1)
	    print(name1)

	except :

	  	# print('There was No Data')
	    cnty_w = np.zeros((dim , dim ,numsub, count_lamb))

	return cnty_w 




# def dti_weight(idx) :

#     data_path = "Dataset/"
#     # Weights = pd.read_csv(data_path + 'foo.csv' ,  header=None)
#     dti = np.load(data_path + 'DTI_dataset.npy')
#     Weights = dti[:,:,idx]
#     We = Weights.to_numpy(dtype= np.float32) 

#     return We



def golem(X, idx , lambda_1, lambda_2, equal_variances=False,
          num_iter=9e+4, learning_rate=3e-5, seed=1,
          checkpoint_iter=None, output_dir=None, B_init=None ):

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    data_path = "Dataset/"

    # Weights = pd.read_csv(data_path + 'foo.csv' ,  header=None)
    # We = Weights.to_numpy(dtype= np.float32) 

    dti = np.load(data_path + '13_Prior_1000chi_164.npy')
    Weights = dti[:,: , idx]
    We = Weights.astype(dtype= np.float32) 
    # We[We == -1000] = -30
    
    #B_init = np.load('Results/' + 'Golem_weights_data_synthetic_300_0.020002.npy')[:,:,idx,0]

    print(We)
    # Center the data
    X = X - X.mean(axis=0, keepdims=True)

    # Set up model
    n, d = X.shape

    model = GolemModel(n, d, lambda_1, We , lambda_2, equal_variances, seed, B_init)

    # Training
    trainer = GolemTrainer(learning_rate)
    for i in range(1) :
    	
    	B_est = trainer.train(model, X, num_iter, checkpoint_iter, output_dir)

    return B_est 


# def run_golem(data , lmbda1 , lastnum , numsub) :

# 	for i3 in trange(lastnum +1 ,numsub):

# 		print('num_sub: ' + str(i3) + '\n')
# 		logging.basicConfig(
# 			level=logging.INFO,
# 			format='%(asctime)s %(levelname)s - %(name)s - %(message)s')
		

# 		set_seed(1)

# 		dataset = data[:,:,i3]

# 		# GOLEM-EV
# 		B_est = golem(dataset, lambda_1= lmbda1 , lambda_2=5.0,
# 			equal_variances=True, checkpoint_iter=5000)
		
# 		cnty_w[:,:,i3]= B_est

# 		name2_mrtx = 'Results/Golem_weights_' + name + '_' + str(lmbda1)
# 		np.save(name2_mrtx ,cnty_w)



# def assign_lambda(data):
# 	for k in range(data.shape[-1]):
# 		temp = data[:,:,:,k].copy()
# 		for k2 in range(temp.shape[-1]) :
# 			if temp[:,:,k2].sum(0).sum(0) != 0 :
# 				last_num = k2 
# 				last_lam = k
# 	return last_num , last_lam


def assign_lambda(data):

    last_num = 0
    last_lam = 0
    for k in range(data.shape[-1]):
        temp = data[:,:,:,k].copy()
        for k2 in range(temp.shape[-1]) :
            if temp[:,:,k2].sum(0).sum(0) != 0 :
                last_num = k2 
                last_lam = k
        
    return last_num , last_lam




# if __name__ == "__main__":  

#   	# c , l = read_Cmrtx('train' , 0.01 , 63 , 0)
#   	c , l = assign_lambda()
#   	print(c.shape)
#   	print(l)

