# python-api-development
repo for this youtube video --> https://www.youtube.com/watch?v=0sOvCWFmrtA

start applicatin on production server: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
execute db migration: alembic upgrade head
