from attr import NOTHING
from matplotlib import pyplot as plt
from streamlit.elements.arrow import Data
from config.config import Configuration as cfg, Data as data, UI as ui
import pandas as pd
import numpy as np
import glob
import streamlit as st

@st.cache(allow_output_mutation=True)
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
    #Transform Data
    data_obj.transform_sessions()
    data_obj.transform_sessionsq()

def build_ui_data(data_obj):
    if ui.sidebar_select == None:
        sidebar_select_data = data_obj.items_tags.tagtype.unique().tolist()
        ui.sidebar_select = sidebar_select_data

def run_app(data_obj):
    #Title
    st.title("Learnosity - User Dashboard")
    st.sidebar.title("Criterion")
    
    #Select an option
    ui.selected = st.sidebar.selectbox("Select a Tag Type", ui.sidebar_select)
    st.header("Session Data")
    st.subheader("by TagType")

    #Build Data
    sessions_data = data_obj.join_selected(ui.selected)
    st.dataframe(data = sessions_data.head())
    st.write("Total Count = ",len(sessions_data.index))

    #Descriptive Statistics
    st.header("Descriptive Statistics")
    st.dataframe(data = sessions_data.describe())

    #Bar Plot
    st.header("Distribution of Scores for "+ui.selected+" tag")
    st.subheader("Questions Scored and Maximum Scores per tagtype")
    st.success("This graph describes scored obtained by a user per tagtype for a tag and the maximum score for questions per tagtype. It entails a\
        fundamental analysis of the chapters that are easy to score and chapters that are difficult to score across the number of users.")
    sessions_data_score = sessions_data[["tag","question_score","question_max_score"]].groupby(["tag"]).sum()
    st.bar_chart(sessions_data_score)

    st.subheader("Questions Attempted per Total Questions for each tagtype")
    st.success("This graph describes the total number of questions attempted vs question not attempted for a particular tagtype. It demonstrates \
        the comparison between number of questions per tagtype and an approximate level of difficlty for not attempting questions")
    sessions_data_qa = sessions_data.pivot_table(index="tag",columns="question_attempted",aggfunc="size",fill_value=0)
    sessions_data_qa_df = pd.DataFrame(sessions_data_qa.to_records()).set_index("tag").rename(columns={"0":"Not_Attempted","1":"Attempted"})
    st.line_chart(sessions_data_qa_df)





    
        
        





