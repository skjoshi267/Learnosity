from attr import NOTHING
from streamlit.elements.arrow import Data
from config.config import Configuration as cfg, Data as data, UI as ui
import pandas as pd
import numpy as np
import glob
import streamlit as st

@st.cache
def load_data():
    file_paths = [(cfg.DATA_PATH + each_file + '*.csv') for each_file in cfg.FILES_TO_LOAD]
    files_list = [glob.glob(path) for path in file_paths]

    file_data = []

    for file in files_list:
        raw_data  = pd.concat([pd.read_csv(file_name,lineterminator = "\n") for file_name in file])
        file_data.append(raw_data)

    return file_data

def assign_data(file_data):
    data_obj = data(file_data)
    return data_obj

def transform_data(data_obj):
    #Transform Tags
    data_obj.transform_tags()

def build_ui_data(data_obj):
    if ui.sidebar_select == None:
        sidebar_select_data = data_obj.tags.tag.unique().tolist()
        ui.sidebar_select = sidebar_select_data

def run_app(data_obj):
    st.title("Learnosity - User Dashboard")
    st.sidebar.title("Criterion")
    ui.selected = st.sidebar.selectbox("Select a Tag for Course", ui.sidebar_select)
    
    st.header("Raw Data")
    st.dataframe(data = data_obj.tags[data_obj.tags.tag == ui.selected])





    
        
        





