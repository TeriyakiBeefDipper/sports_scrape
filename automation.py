#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 20:20:50 2023

@author: tbd
"""

import subprocess
import time
import datetime

scrape_script = 'scrape.py'

now = datetime.datetime.now()
today = datetime.datetime.now().date()
end_time = datetime.datetime.combine(today+datetime.timedelta(days=1), datetime.time.min)


while now < end_time:
    subprocess.call(['python',scrape_script])
    
    time.sleep(900)
    
# print(now)
# print(today)
# print(end_time)