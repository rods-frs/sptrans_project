#learned with AI | All human code including logic and comments

import pandas as pd
import tools
import data_extraction

routes_df = tools.read_csv("data/routes.csv")
routes_df = routes_df[['route_id', 'route_long_name', 'route_color']]

trips_df = tools.read_csv("data/trips.csv")
trips_df = trips_df[['route_id', 'service_id']]

trip_duration_df = data_extraction.get_trip_duration()

final_df = pd.merge(routes_df, trips_df, on="route_id")
final_df['merge_key'] = final_df['route_id']
final_df = final_df.merge(trip_duration_df, on="merge_key")
final_df = final_df.drop(columns={'trip_start_ida', 'trip_end_ida', 'trip_end_volta', 'trip_start_volta'})

final_df = final_df.drop_duplicates()

print(tools.check_str_contains(final_df, 'route_id','7903'))

print(final_df)


