@echo off
REM Install dependencies
pip install -r requirements.txt

REM Install gunicorn for production
pip install gunicorn

REM Run with production WSGI server
gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app

REM To keep running in background:
REM Use Task Scheduler to run this batch file on startup
