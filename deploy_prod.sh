#!/bin/sh
ssh ubuntu@3.92.234.28 <<EOF
  cd calorietracker
  git pull
  pip install -r requirements.txt
  ./manage.py migrate
  exit
EOF