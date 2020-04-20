#!/bin/bash
exitCode=2
while [ $exitCode -ge 2 ]
do
    sudo python3 puggerbot.py $1
    exitCode=$?
    echo Puggerbot exited with code $exitCode.
    if [ $exitCode -eq 3 ]
    then
        git pull
    fi
    if [ $exitCode -eq 4 ]
    then
        git pull
        sudo rm DnD_5e.db
    fi
done
