from datetime import datetime

def toTimestamp(d):
    return int(datetime.timestamp(d))