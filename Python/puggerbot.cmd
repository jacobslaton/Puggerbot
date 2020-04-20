@echo off
:puggerbot
python puggerbot.py %1
if %errorlevel%==2 goto :puggerbot


