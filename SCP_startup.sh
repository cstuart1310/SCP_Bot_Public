#!/bin/bash

echo "Starting Scripts"
screen -d -S annie -m python3 SCP_Bot_Git.py
screen -d -S freddy -m python3 get_followers.py
echo "Done"
