#Set working directory for power bi
##This was very difficult
import sys
import os
sys.path.insert(0, r'C:\Users\clone\Documents\LolDashboard')
os.chdir(r'C:\Users\clone\Documents\LolDashboard')

#Power BI is very VERY particular about this
from riot_auth import developer_api_key
import pandas as pd
#ALSO riot has api limits, 
import time
from lg_stats import first_function
from rank import second_function
from lg_events import third_function

df1 = first_function(developer_api_key)
#sleep for 1 second...
time.sleep(1)
#call method from: rank.py
rank_df2 = second_function(developer_api_key)

events_df3 = third_function()