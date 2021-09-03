from matplotlib import pyplot as plt
from matplotlib.colors import NoNorm
from config.config import Configuration as cfg, Data as data, UI as ui
import pandas as pd
import numpy as np
import glob
import streamlit as st
import altair as alt

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

    #Build User
    ui.user_select = sessions_data["user_id"].unique().tolist()
    ui.user = st.sidebar.selectbox("Select a User", ui.user_select)
    user_data = data_obj.user_data(ui.user)

    #Descriptive Statistics
    st.header("Descriptive Statistics")
    st.dataframe(data = sessions_data.describe())

    #Bar Plot
    st.header("Distribution of Scores for "+ui.selected+" tag")
    st.subheader("Questions Scored and Maximum Scores per tagtype")
    st.success("This graph describes scored obtained by a user per tagtype for a tag and the maximum score for questions per tagtype. It entails a\
        fundamental analysis of the chapters that are easy to score and chapters that are difficult to score across the number of users.")
    sessions_data_score = sessions_data[["tag","question_score","question_max_score"]].groupby(["tag"]).sum()
    st.line_chart(sessions_data_score)

    #Line Plot
    st.subheader("Questions Attempted v/s Questions, Not Attempted for each tagtype")
    st.success("This graph describes the total number of questions attempted vs question not attempted for a particular tagtype. It demonstrates \
        the comparison between number of questions per tagtype and an approximate level of difficlty for not attempting questions")
    sessions_data_qa = sessions_data.pivot_table(index="tag",columns="question_attempted",aggfunc="size",fill_value=0)
    sessions_data_qa_df = pd.DataFrame(sessions_data_qa.to_records()).set_index("tag").rename(columns={"0":"Not_Attempted","1":"Attempted"})
    st.bar_chart(sessions_data_qa_df)

    #Scatter Plot
    st.subheader("Scatter Plot: Count of Total Sessions vs Total Scores")
    st.warning("This graph describes the relationship between rate of change in total scores per tagtype as the overall rate of sessions increase or decrease\
        It dsisplays the positive correlation between the total sessions and scores of all the users. Hence, it can be proved that more sessions in a\
            tagtype do improve the scores slightly")
    total_sessions = sessions_data[["session_id","tag"]].groupby("tag").count().reset_index()
    total_scores = sessions_data_score.reset_index()
    total_scores["score_percent"] = (total_scores["question_score"] / total_scores["question_max_score"]) * 100
    scatter_data = total_sessions.merge(total_scores, on="tag")
    scatter = alt.Chart(scatter_data).mark_circle(size = 60).encode(
        x = "score_percent:Q",
        y = "session_id:Q"
    ).interactive()
    st.altair_chart(scatter,use_container_width = True)

    #Trend Analysis
    st.subheader("Trend Analysis for user: "+str(ui.user))
    st.write("Filter by TagType")
    user_data = user_data[["session_dt_started","tag","question_score","question_max_score"]].groupby(["session_dt_started","tag"]).sum()
    user_data["score_percent"] = (user_data["question_score"] / user_data["question_max_score"]) * 100
    user_data = user_data.reset_index().set_index("session_dt_started")
    tagtype = st.selectbox("Select a tagtype",user_data["tag"].unique().tolist())
    
    st.success("This graph describes the relationship between the percent score for all the tagtypes of a particular user\
        It is a raw time series plot of the total score across all the sessions on a specific date allowing users to identify increase/decrease in their performace\
            and investigate their scores across a timeframe")
    filter_data = user_data[user_data["tag"] == tagtype]
    st.line_chart(filter_data["score_percent"],use_container_width = True)


    # demo = alt.Chart(user_data).mark_line().encode(
    #     x = "tag:N",
    #     y = "score_percent:Q"
    # ).interactive()
    # st.altair_chart(demo,use_container_width = True)












    
        
        





