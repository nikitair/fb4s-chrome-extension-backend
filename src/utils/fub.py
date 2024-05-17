from datetime import datetime


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')


def get_default_task_dueDateTime():
    return datetime.now().strftime("%Y-%m-%dT23:00:00") + " -01:00"
