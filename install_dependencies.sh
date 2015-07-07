#!/usr/bin/env bash


pythonversion=$(python -c 'import sys; print("%d.%d.%d" % (sys.version_info[0], sys.version_info[1], sys.version_info[2]))')

if [[ $pythonversion =~ ^3.*$ ]]; then
	echo "Install dependencies using Python 3"
	pip3 install -r chassis/development.txt
fi

if [[ $pythonversion =~ ^2.*$ ]]; then
	echo "Install dependencies using Python 2"
	pip install -r chassis/development.txt
fi
