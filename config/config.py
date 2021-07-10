class Configuration:
    DATA_PATH = "data/"
    FILES_TO_LOAD = ["sessions-","sessionsquestions-"] #"tags","activites","items"]


class Data:
    sessions = ""
    session_questions = ""
    tags = ""
    activities = ""
    items = ""

    def assign_data(i, raw_data):
        if i == 0:
            __class__.sessions = raw_data
        elif i == 1:
            __class__.session_questions = raw_data
        elif i == 2:
            __class__.tags = raw_data
        elif i == 3:
            __class__.activities = raw_data
        elif i == 4:
            __class__.items = raw_data

