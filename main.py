#learned with AI | All human code including logic and comments

import pandas as pd
import tools

raw_data = tools.read_csv("data/stop_times.csv") #get the CSV data

min_stops = raw_data.groupby("trip_id")["stop_sequence"].min() #get the first stop time, min() prevents dupplicates
min_stops = pd.merge(min_stops, raw_data, on=['trip_id', 'stop_sequence']) #get only the rows which the data is from the first stop

start_time = min_stops[['trip_id', 'arrival_time']] #get only the trip_id and arrival_time columns
start_time['arrival_time'] = pd.to_timedelta(start_time['arrival_time']) #transform the arrival_time into timedelta (cant be normal datetime because value can be >=24h)
start_time = start_time.rename(columns={'arrival_time':'trip_start'}) #rename the column for better view

max_stops = raw_data.groupby("trip_id")["stop_sequence"].max() #get the last trip from each trip_id
max_stops = pd.merge(max_stops, raw_data, on=['trip_id', 'stop_sequence']) #get only the rows which the data is from the last stop

final_time = max_stops[['trip_id', 'arrival_time']] #removes unnecessary columns
final_time = final_time.rename(columns={'arrival_time':'trip_end'}) #rename column for better view
final_time['trip_end'] = pd.to_timedelta(final_time['trip_end']) #transform arrival_time to timedelta for the same reason as before

result = pd.merge(start_time, final_time, on="trip_id") #merge the start and final tables to get the start and end of a trip in deltatime
result['trip_duration'] = result['trip_end'] - result['trip_start'] #get the difference to get the trip duration
result['trip_duration'] = result[result['trip_duration'] < pd.Timedelta(0)] + pd.Timedelta(days=1) #trips that finished after 12am would get negative deltas, so this adds 1 day to it

