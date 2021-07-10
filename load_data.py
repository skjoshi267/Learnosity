from config.config import Configuration as cfg, Data as data
import pandas as pd
import numpy as np
import glob

def load_data():
    file_paths = [(cfg.DATA_PATH + each_file + '*.csv') for each_file in cfg.FILES_TO_LOAD]
    files_list = [glob.glob(path) for path in file_paths]
    i =  0
    for file in files_list:
        data.assign_data(i,pd.concat([pd.read_csv(file_name) for file_name in file]))
        i+= 1




    
        
        





