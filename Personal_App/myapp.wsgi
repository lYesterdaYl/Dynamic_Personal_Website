#!/usr/bin/python3.6
import sys
sys.path.insert(0,"/var/www/Personal_App/")
sys.path.insert(0,"/var/www/Personal_App/personal_app/")
from personal_app import app as application

application.secret_key = "secret_key"