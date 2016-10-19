from setuptools import setup

setup(
    name = "celerybeat-redis",
    description = "A Celery Beat Scheduler that uses Redis to store both schedule definitions and status information",
    version = "0.1.6",
    license = "Apache License, Version 2.0",
    author = "Kong Luoxing",
    author_email = "kong.luoxing@gmail.com",
    home_page = 'https://github.com/raynaya/celerybeatredis/',
    maintainer = "Shamik Ray",
    maintainer_email = "shamik.ray@coviam.com",

    keywords = "python celery beat redis",

    packages = [
        "celerybeatredis"
    ],

    install_requires=[
        'setuptools',
        'redis>=2.10.3',
        'celery>=3.1.23'
    ]

)
