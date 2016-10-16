# Project Status

Because of the busy of work, I doesn't got much time on this time, and one major reason is now I am programming with Java...
So I won't push any new release from now on, if someone is interest with it, just fork and maintenance your own version,
Sorry for the inconvenient.

# celerybeat-redis

It's modified from celerybeat-mongo (https://github.com/zakird/celerybeat-mongo)

See Changelog in [CHANGES.md](./CHANGES.md)

This is a Celery Beat Scheduler (http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html)
that stores both the schedules themselves and their status
information in a backend Redis database.

# Features

1. Full-featured celery-beat scheduler
2. Dynamically add/remove/modify tasks
3. Support multiple instance by Active-Standby model

# Installation

It can be installed by
installing the celerybeat-redis Python egg:

    # pip install celerybeat-redis

And specifying the scheduler when running Celery Beat, e.g.

    $ celery beat -S celerybeatredis.schedulers.RedisScheduler

# Configuration

Settings for the scheduler are defined in your celery configuration file
similar to how other aspects of Celery are configured

    CELERY_REDIS_SCHEDULER_URL = "redis://localhost:6379/1"
    CELERY_REDIS_SCHEDULER_KEY_PREFIX = 'tasks:meta:'

You must make sure these two values are configured. `CELERY_REDIS_SCHEDULER_URL`
is used to store tasks. `CELERY_REDIS_SCHEDULER_KEY_PREFIX` is used to generate
keys in redis. The keys will be of the form

    tasks:meta:task-name-here
    tasks:meta:test-fib-every-3s

There is also an optional setting 

    CELERY_REDIS_SCHEDULER_LOCK_TTL = 30

This value determines how long the redis scheduler will hold on to it's lock,
which prevents multiple beat instances from running at the same time. However,
in some cases -- such as a hard crash -- celery beat will not be able to clean
up after itself and release the lock. Therefore, the lock is given a
configurable time-to-live, after which it will expire and be released, if it is
not renewed by the beat instance that acquired it. If said beat instance does
die, another instance will be able to pick up the baton, as it were, and run
instead.

# Quickstart

After installed and configure the needs by above, you can make a try with test, cd to test directory, start a worker by:

    $ celery worker -A tasks -l info

then start the beat by:

    $ celery beat -S celerybeatredis.schedulers.RedisScheduler

celerybeat-redis will load the entry from celeryconfig.py

# Detailed Configuration

There was two ways to add a period task:

## Add in celeryconfig.py

Celery provide a `CELERYBEAT_SCHEDULE` entry in config file, when
celerybeat-redis starts with such a config, it will load tasks to redis, create
them as a celerybeat-redis task.

It's perfect for quick test

## Manaully add to Redis

You can create task by insert specify data to redis like the following:



Schedules can be manipulated in the Redis database through
direct database manipulation. There exist two types of schedules,
interval and crontab(not working currently).

The example from Celery User Guide::Periodic Tasks.
```python
CELERYBEAT_SCHEDULE = {
    'interval-test-schedule': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (param1, param2)
    }
}
```

Becomes the following::
```json
{
    "name" : "interval test schedule",
    "task" : "task.add",
    "enabled" : true,
    "schedule" : {
        "every" : 30,
        "period" : "seconds",
    },
    "args" : [
        "param1",
        "param2"
    ]
}
```
The following command should add a task in redis. Any task in celeryconfig is also added to the redis db if already not present.

```
set tasks:meta:multiply-every-10-minutes "{\"name\":\"multiply-every-10-minutes\",\"task\":\"tasks.multiply\",\"enabled\":true,\"schedule\": { \"period\": \"minutes\", \"every\": 10 },\"args\":[\"3\",\"2\"] }"
```

The following fields are required: name, task, crontab || interval,
enabled when defining new tasks.
`total_run_count` and `last_run_at` are maintained by the
scheduler and should not be externally manipulated.

The example from Celery User Guide::Periodic Tasks.
(see: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules)

Similarly a crontab schedule becomes like this  - 

```python
CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```

Becomes:

```json
{
    "name" : "add-every-monday-morning",
    "task" : "tasks.add",
    "enabled" : true,
    "schedule" : {
        "minute" : "30",
        "hour" : "7",
        "day_of_week" : "1",
        "day_of_month" : "*",
        "month_of_year" : "*"
    },
    "args" : [
        "16",
        "16"
    ]
}
```
# Deploy multiple nodes

Original celery beat doesn't support multiple node deployment, multiple beat
will send multiple tasks and make worker duplicate execution, celerybeat-redis
use a redis lock to deal with it. Only one node running at a time, other nodes
keep tick with minimal task interval, if this node down, when other node
ticking, it will acquire the lock and continue to run.

WARNING: this is an experiment feature, need more test, not production ready at
this time.
