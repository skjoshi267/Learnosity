import pandas as pd
import numpy as np

class Configuration:
    DATA_PATH = "data/"
    FILES_TO_LOAD = ["sessions-","sessionsquestions-","tags","activities","items"]

class Data:
    def __init__(self, raw_data):
        self.sessions = raw_data[0]
        self.session_questions = raw_data[1]
        self.tags = raw_data[2]
        self.activities = raw_data[3]
        self.items = raw_data[4]

    def transform_tags(self):
        tags = self.tags
        tags = tags[tags.tagtype == "COURSE"]
        indexes = tags[tags.tag == "-"].index
        self.tags = tags.drop(indexes, axis = 0).reset_index(drop = True)

class UI:
    sidebar_select = None
    selected = None

