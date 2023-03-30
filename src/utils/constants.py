from datetime import datetime, timedelta

STRTIMEFORMAT = '%Y-%m-%dT%H:%M:%SZ'
TODAY = datetime(
  datetime.now().year,
  datetime.now().month,
  datetime.now().day,
  datetime.now().hour,
  datetime.now().minute,
  datetime.now().second,
)
TWO_DAYS_AGO = TODAY - timedelta(days = 2)
TWO_DAYS_LATER = TODAY + timedelta(days = 2)