from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/students/hemamgholizadeh/MyFoodGRS/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/students/hemamgholizadeh/MyFoodGRS/access_log'
errorlog =  '/home/students/hemamgholizadeh/MyFoodGRS/error_log'
