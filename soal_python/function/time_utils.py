from datetime import datetime, timedelta, timezone

def getTimeinTimezone(offset_hours):
    d = datetime.now()
    tz = timezone(timedelta(hours=offset_hours))
    return d.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

def getTimeUTC():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
