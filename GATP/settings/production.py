# -*- coding: utf-8 -*-
"""
 * @Description:   生产环境配置
 * @version         V1.0
 * @Date           2018年04月10日
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'GATP',
        'USER': 'root',
        'PASSWORD': 'yJviBiHK81EwMEBl',
        'HOST': '10.40.2.192',
        'PORT': '3306',
    }

}

"""
############################################
# mongoengine config
############################################
import mongoengine
mongoengine.connect(host='mongodb://autotest:yJviBiHK81EwMEBl@10.40.2.192:27017/cloudtest')

############################################
# celery config is below
############################################
import djcelery
djcelery.setup_loader()


BROKER_URL = 'amqp://guest:guest@10.40.2.192:5672/'
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 30

CELERY_RESULT_BACKEND = 'mongodb'
CELERY_MONGODB_BACKEND_SETTINGS = { 
    'host': '10.40.2.192',
    'port': 27017,
    'database': 'celery',
    'user': 'autotest',
    'password': 'yJviBiHK81EwMEBl',
    'taskmeta_collection': 'teskmeta',
    'options': {
        'connect': False,
    }
}
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES = 18000
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ENABLE_UTC = False
CELERY_TRACK_STARTED = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_DISABLE_RATE_LIMITS = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_EVENT_QUEUE_TTL = 60
CELERY_EVENT_QUEUE_EXPIRES = 60
CELERYD_TASK_TIME_LIMIT = 18000
CELERYD_MAX_TASKS_PER_CHILD = 50

RETRY = 10

from kombu import Queue, Exchange

CELERY_CREATE_MISSING_QUEUES = False
CELERY_DEFAULT_QUEUE = 'cloudtest_default_celery'
CELERY_DEFAULT_EXCHANGE = 'cloudtest_default_celery'
CELERY_DEFAULT_ROUTING_KEY = 'cloudtest.default.celery'

CELERY_QUEUES = (
    Queue('cloudtest_default_celery', Exchange('cloudtest_default_celery'), routing_key='cloudtest.default.celery'),
    Queue('cloudtest_app_task', Exchange('cloudtest_app'), routing_key='cloudtest.app.task')
)

CELERY_ROUTES = {
    'backend.web.tasks.run_task': {'queue': 'cloudtest_app_task', 'routing_key': 'cloudtest.app.task'},
    'backend.web.tasks.run_device': {'queue': 'cloudtest_app_task', 'routing_key': 'cloudtest.app.task'}
}
"""