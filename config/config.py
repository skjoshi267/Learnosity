import pandas as pd
import numpy as np

class Configuration:
    DATA_PATH = "data/"
    FILES_TO_LOAD = ["sessions-","sessionsquestions-","items_tags","activities","items"]
    DATE_COLUMNS = ["session_dt_started","session_dt_completed","question_dt_created","question_dt_updated"]

class Data:
    def __init__(self, raw_data):
        self.sessions = raw_data[0]
        self.session_questions = raw_data[1]
        self.items_tags = raw_data[2]
        self.activities = raw_data[3]
        self.items = raw_data[4]

    def transform_sessions(self):
        #Transform Sessions Data
        temp_sessions = self.sessions.drop(["activity_id","session_dt_saved","user_dt_created","activity_template_id","item_pool_id","current_time"], axis=1)
        for dt_type in Configuration.DATE_COLUMNS:
            if dt_type in temp_sessions.columns.tolist():
                temp_sessions[dt_type] = pd.to_datetime(temp_sessions[dt_type])
            else:
                pass
        self.sessions = temp_sessions
    
    def transform_sessionsq(self):
        #Transform Sessions Questions
        temp_sessionsq = self.session_questions#.drop(["activity_id","session_dt_saved","user_dt_created","activity_template_id","item_pool_id","current_time"], axis=1)
        for dt_type in Configuration.DATE_COLUMNS:
            if dt_type in temp_sessionsq.columns.tolist():
                temp_sessionsq[dt_type] = pd.to_datetime(temp_sessionsq[dt_type])
            else:
                pass
        self.sessionsq = temp_sessionsq

    def join_selected(self,tagtype):
        #Join Data of Sessions, SessionsQuestions and Item Tags
        filter_data = self.items_tags[self.items_tags.tagtype == tagtype]
        join_data = self.session_questions.merge(filter_data, on="item_reference")
        self.sessions_db = self.sessions.merge(join_data, on=["session_id","user_id"])
        return self.sessions_db

class UI:
    sidebar_select = None
    selected = None

