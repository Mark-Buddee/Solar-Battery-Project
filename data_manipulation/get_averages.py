import pandas as pd
import numpy as np
from pathlib import Path


def init():
    # Create output arrays

    # Load annual average
    load_annual_avg = np.zeros((510, 24))
    #
    #       household_number:       (0, 509)
    #       hour of the day:        (0, 23)
    #
    #       [household number][hour of the day]

    # Load and Generation seasonal averages
    load_seasonal_avg = np.zeros((3, 24, 510))
    gen_seasonal_avg = np.zeros((3, 24, 510))
    #
    #       season:                 {0: summer, 1: winter, 2:else}
    #       hour of the day:        (0, 23)
    #       household_number:       (0, 509)

    #       [season][hour of the day][household number]

    # Note: the household number for a particular house corresponds to the row index of the household's site_id within
    # the file 'site_details_USYD_202010.csv' although this can be changed very easily

    return load_annual_avg, load_seasonal_avg, gen_seasonal_avg


def get_season(day_of_year):

    # Summer: 1st Nov -> 31st March inclusive
    if (day_of_year >= 305) or (day_of_year <= 90):
        return 0  # summer

    # Winter: 1st June -> 31st August inclusive
    if (day_of_year >= 152) and (day_of_year <= 243):
        return 1  # winter

    return 2  # off-season


# Initialise output arrays
load_annual_avg, load_seasonal_avg, gen_seasonal_avg = init()

# Create a dictionary, linking site ID to timezone ID
sites_df = pd.read_csv("metadata/site_details_USYD_202010.csv", index_col=0, usecols=['site_id', 'timezone_id'])
sites_dict = sites_df.transpose().to_dict(orient='records')[0]

# Create a list of site ids
sites = list(sites_dict.keys())

# Read the combined data
data_df = pd.read_csv("data/combined_data.csv")

for household_num, site_id in enumerate(sites):

    # Get the site data
    site_data_df = data_df.loc[data_df['site_id'] == site_id].reset_index(drop=True)

    # Get the timezone
    timezone_id = sites_dict.get(site_id)

    # Convert utc timestamps (strings) to local time (datetime objects)
    utc_timestamps = pd.Series(site_data_df['utc_timestamp'])
    utc_timestamps_dt = pd.to_datetime(utc_timestamps, format='%Y-%m-%d %H:%M:%S+00:00')  # Create datetime objects
    utc_timestamps_dt = utc_timestamps_dt.dt.tz_localize(tz='UTC')  # Make datetime objects timezone-aware
    local_timestamps_dt = utc_timestamps_dt.dt.tz_convert(tz=timezone_id)  # Convert times to local time

    # Store the local timestamps in place of the utc timestamps
    site_data_df = site_data_df.rename(columns={'utc_timestamp': 'local_timestamp'})
    site_data_df['local_timestamp'] = local_timestamps_dt

    # Store the local hour
    site_data_df['local_hour'] = local_timestamps_dt.dt.hour

    # Store the local season
    day_of_year = site_data_df['local_timestamp'].dt.dayofyear
    season = day_of_year.apply(get_season)
    site_data_df['season'] = season

    # ANNUAL AVERAGE LOAD #

    # Get load data
    load_df = site_data_df.loc[site_data_df['con_type'] == 'total_load'].reset_index(drop=True)

    for hour in range(24):

        # Get the energy column for the particular hour
        hour_values_df = load_df.loc[load_df['local_hour'] == hour].reset_index(drop=True)
        values_to_avg_df = hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Date entries are power produced/used in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        load_annual_avg[household_num][hour] = hourly_average

    # SEASONAL AVERAGE LOAD #

    for hour in range(24):

        # SUMMER #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = load_df.loc[load_df['local_hour'] == hour].reset_index(drop=True)
        summer_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 0]
        values_to_avg_df = summer_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power used in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        load_seasonal_avg[0][hour][household_num] = hourly_average  # 0 represents summer

        # WINTER #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = load_df.loc[load_df['local_hour'] == hour].reset_index(drop=True)
        winter_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 1]
        values_to_avg_df = winter_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power used in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        load_seasonal_avg[1][hour][household_num] = hourly_average  # 1 represents winter

        # OFF SEASON #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = load_df.loc[load_df['local_hour'] == hour].reset_index(drop=True)
        offseason_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 2]
        values_to_avg_df = offseason_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power used in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        load_seasonal_avg[2][hour][household_num] = hourly_average  # 2 represents off season

    # SEASONAL AVERAGE GENERATION #

    # Get generation data
    generation_df = site_data_df.loc[site_data_df['con_type'] == 'pv_generation'].reset_index(drop=True)

    for hour in range(24):

        # SUMMER #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = generation_df.loc[generation_df['local_hour'] == hour].reset_index(drop=True)
        summer_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 0]
        values_to_avg_df = summer_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power produced in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        gen_seasonal_avg[0][hour][household_num] = hourly_average  # 0 represents summer

        # WINTER #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = generation_df.loc[generation_df['local_hour'] == hour].reset_index(drop=True)
        winter_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 1]
        values_to_avg_df = winter_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power produced in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        gen_seasonal_avg[1][hour][household_num] = hourly_average  # 1 represents winter

        # OFF SEASON #
        # Get the energy column for the particular hour for the particular season
        hour_values_df = generation_df.loc[generation_df['local_hour'] == hour].reset_index(drop=True)
        offseason_hour_values_df = hour_values_df.loc[hour_values_df['season'] == 2]
        values_to_avg_df = offseason_hour_values_df['energy_(Wh)']

        # Compute hourly average
        five_min_mean = values_to_avg_df.mean()  # Data entries are power produced in a 5 minute interval
        hourly_average = 12 * five_min_mean

        # Save to output array
        gen_seasonal_avg[2][hour][household_num] = hourly_average  # 2 represents off season

# Save load annual average as csv file
filepath = Path('data/results/load_annual_avg.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
np.save(filepath, load_annual_avg)

# Save load seasonal average as csv file
filepath = Path('data/results/load_seasonal_avg')
filepath.parent.mkdir(parents=True, exist_ok=True)
np.save(filepath, load_seasonal_avg)

# Save generation seasonal average as csv file
filepath = Path('data/results/gen_seasonal_avg')
filepath.parent.mkdir(parents=True, exist_ok=True)
np.save(filepath, gen_seasonal_avg)
