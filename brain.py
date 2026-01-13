#Set working directory for power bi
import os
os.chdir(r'C:\Users\clone\Documents\LolDashboard')

#we need the developer api key
from riot_auth import developer_api_key

#do we need pandas in EVERY file?
import pandas as pd

#ALSO riot has api limits, 
import time

#call method from: lg_stats.py
from lg_stats import first_function
df1 = first_function(developer_api_key)

#sleep for 1 second...
time.sleep(1)

#call method from: rank.py
from rank import second_function
df2 = second_function(developer_api_key)