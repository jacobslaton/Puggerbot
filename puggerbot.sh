#!/bin/bash
exitCode=2
while [ $exitCode -eq 2 ]
do
	git pull
	node Source/index %1
	node Source/exit_code
	exitCode=$?
done
