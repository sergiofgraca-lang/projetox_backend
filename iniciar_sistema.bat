@echo off
cd /d C:\projetox_backend

start "" chrome --app=http://127.0.0.1:8000

venv\Scripts\python.exe manage.py runserver