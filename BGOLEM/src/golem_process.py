import os

from models import GolemModel
from trainers import GolemTrainer
import numpy as np 

def golm_process(name):
    # Minimal code to run GOLEM.
    import logging

    from data_loader import SyntheticDataset
    from utils.train import postprocess
    from utils.utils import count_accuracy, set_seed
    
    #name = 'Golem_weights_SF7_150_dataset_0.001001bayses'
    B_EST = np.load("Results/" + name +  '.npy')
    B_Pro = np.zeros(B_EST.shape)
    
    for la in range(B_EST.shape[-1]) :
        for sub in range(B_EST.shape[-2]) :
    	    B_est = B_EST[:,:,sub,la]
    	    B_processed = postprocess(B_est, graph_thres=0.1)
    	    print(B_processed.sum())
    	
    	    B_Pro[:,:,sub,la] = B_processed 

 
    # Post-process estimated solution and compute results
    
    test_golem_add = '/home/mlcm-cpu/Documents/Mehdi/Golem/test_golem_results/'
    
    np.save('Results/Connectivity_' + name , B_Pro)
    np.save(test_golem_add + 'Connectivity_' + name , B_Pro)
    
    
    
    
if __name__ == '__main__' :
    
    file1 = 'Golem_weights_SF7_75_dataset_0.0010108bayses'
    golm_process(file1)

