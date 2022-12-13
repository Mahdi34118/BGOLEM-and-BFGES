import numpy as np
import os 
from data_loader import SyntheticDataset
from utils.train import postprocess
from utils.utils import count_accuracy, set_seed

path = 'Results/'


x = np.load( path + 'Golem_weights_SF7_150_dataset_1bayses.npy')

print(x.shape)
B_postproc = np.zeros(x.shape)

for idx in range(0,x.shape[-1]):

	for jdx in range(1,x.shape[-2]):


		B_est = x[:,:,jdx , idx]
		B_proces = postprocess(B_est, graph_thres=0.3)

		B_proces[B_proces!=0] = 1
		B_postproc[:,:,jdx , idx] = B_proces





np.save(path+"Golem_Binary_train_sf7_bayes" , B_postproc)





