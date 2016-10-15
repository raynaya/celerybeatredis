from datetime import timedelta
from celery.schedules import crontab
CELERY_REDIS_SCHEDULER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_URL = "redis://localhost:6379/0"
CELERY_REDIS_SCHEDULER_KEY_PREFIX = "tasks:meta:"
CELERYBEAT_SCHEDULE = {
    'add-every-40-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=40),
        'args': (16, 16)
    },
    'multiply-every-30-seconds': {
        'task': 'tasks.multiply',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
    'subtract-every-3-minutes': {
        'task': 'tasks.subtract',
        'schedule': timedelta(minutes=3),
        'args': (20, 10),
    },
    'subtract-every-35-minutes': {
        'task': 'tasks.subtract',
        'schedule': timedelta(minutes=35),
        'args': (40, 10),
    },
    'subtract-every-midnight': {
        'task': 'tasks.subtract',
        'schedule': crontab(minute=0, hour=0),
        'args': (100, 50),
    },


}
