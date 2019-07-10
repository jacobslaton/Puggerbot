@echo off
:puggerbot
node Source/index %1
node Source/exit_code
if %errorlevel%==2 (
	git pull
	goto :puggerbot
)
