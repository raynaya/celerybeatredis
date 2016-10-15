from celery import Celery
import time

app = Celery()
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    time.sleep(3)
    return x + y
@app.task
def multiply(x, y):
    time.sleep(3)
    return x * y

@app.task
def subtract(x, y):
	return x-y