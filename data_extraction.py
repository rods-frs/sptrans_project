import pandas as pd
import tools

def get_trip_duration():
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

    mask = result['trip_duration'] < pd.Timedelta(0) #create a mask with all timedeltas that passes 24 hours format -> Trips that finished after 0h
    result.loc[mask, 'trip_duration'] += pd.Timedelta(days=1) #adds 1 day to the timedeltas that passes the 24 hours format -> better viewing and processing

    ida_mask = result['trip_id'].astype(str).str[-1] == "0" #puts in a mask all trip_id's of "ida"
    ida_df = result[ida_mask] #creates a df with only "ida" trips
    volta_df = result[~ida_mask] #creates a df with only "volta" trips

    volta_df['merge_key'] = volta_df['trip_id'].astype(str).str[:-2] #creates a merge_key column because the trip_id has 2 digits difference between "ida" and "volta" -> removes the last 2 digits which are the difference
    ida_df['merge_key'] = ida_df['trip_id'].astype(str).str[:-2] #same as last line

    final_result = pd.merge(ida_df, volta_df, on="merge_key", suffixes=('_ida', '_volta'), how="left") #merges the two maintaining circular routes by doing a left merge

    return final_result
