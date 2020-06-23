import time
import pandas as pd
import numpy as np

CITY_CHICAGO = 'chicago'
CITY_NYC = 'new york city'
CITY_WASHINGTON = 'washington'

MONTHS_ALL = -1
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']


def month_name(month):
    """
    Returns name of the month.

    Args:
        (int) month - number of a month
    Returns:
        (str) str - Capitalized name of a given month
    """
    return MONTHS[month - 1].capitalize()


WEEKDAYS_ALL = -1
WEEKDAYS = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']


def weekday_name(day):
    """
    Returns name of the week.

    Args:
        (int) day - number of a week day
    Returns:
        (str) str - Capitalized name of a given week day
    """
    return WEEKDAYS[day].capitalize()


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def format_hour(hour):
    """
    Returns formatted hour name in a 12-hour format (including AM/PM).

    Args:
        (int) hour - day hour in 24 hours format
    Returns:
        (str) formatted_hour - formatted 12-hour string
    """
    if hour == 0:
        formatted_hour = '12 AM'
    elif hour == 12:
        formatted_hour = '12 PM'
    else:
        t = 'AM' if hour < 12 else 'PM'
        formatted_hour = '{} {}'.format(hour, t)

    return formatted_hour


def format_seconds(secs):
    """
    Returns more readable version of the seconds value,
    converting them to hours : minuts : seconds format.

    Args:
        (int) seconds - value of seconds to format
    Returns:
        (str) formatted_seconds - formatted seconds string
    """

    if isinstance(secs, int):
        minutes, seconds = divmod(secs, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        formatted_seconds = ''

        if days > 0:
            formatted_seconds += '{} days, '.format(days)
        if hours > 0:
            formatted_seconds += '{} hours, '.format(hours)
        if minutes > 0:
            formatted_seconds += '{} minutes and '.format(minutes)

        formatted_seconds += '{} seconds'.format(seconds)
    else:
        formatted_seconds = '(wrong value provided)'

    return formatted_seconds

# Definitions


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # DONE: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    # DONE: get user input for month (all, january, february, ... , june)
    month = get_month()
    # DONE: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    print('-'*40)
    return city, month, day


def get_city():
    """
    Requests user to provide a city name.

    Returns:
        (str) city - name of the city to analize the data for.
    """
    # Requesting city name from the user. We can use short or full version of a name of a city.
    while True:
        user_city = input('\nWhich city would you like to get your stats on?\n' +
                          'Select one of:\n "[C]hicago", "[N]ew York City" or "[W]ashington":\n')
        if user_city.lower() == 'c' or user_city.lower() == 'chicago':
            city = CITY_CHICAGO
            break
        elif user_city.lower() == 'n' or user_city.lower() == 'new york city':
            city = CITY_NYC
            break
        elif user_city.lower() == 'w' or user_city.lower() == 'washington':
            city = CITY_WASHINGTON
            break
        else:
            # When wrong name is selected, we print the note to the user run the loop once again.
            print('You entered "{}", but it is not a valid option. Please select a valid name as shown.'.format(
                user_city))
            continue

    print('You selected "{}". So I will use it in my analysis!'.format(city))

    return city


def get_month():
    """
    Requests user to provide a month number, or 'a' for not using months filter.

    Returns:
        (str) month - name of the month to analyze the data for, or 'all' to skip this filter.
    """
    # First check whether we should use months for filters
    while True:
        filter_type = input(
            'Do you want to [f]ilter the data by month or use [a]ll months?\n').lower()
        if filter_type == 'f':
            # If we do, ask for which month
            while True:
                try:
                    user_month = int(
                        input('Which month should we use (1 - January, ..., 6 - June)?\n'))
                except ValueError:
                    print("Please, use numbers only.")
                    continue

                if user_month in range(1, 7):
                    month = user_month
                    print('You selected "{}", meaning {}. So I will use it in my analysis!'.format(
                        month, month_name(month).capitalize()))
                    break
                else:
                    print('You entered "{}", but it is not a valid option. Please select a  number between 1 and 6.'.format(
                        user_month))
            break
        # Or we use 'all' for not using filters
        elif filter_type == 'a':
            month = MONTHS_ALL
            print(
                'Fine, I will not use any filters for months. We will use all available data')
            break
        else:
            print('You entered "{}", but it is not a valid option. Please select a valid option as shown.'.format(
                filter_type))
            continue

    return month


def get_day():
    """
    Requests user to provide a day number for filtering, or 'a' for not using days filter.

    Returns:
        (str) day - name of the day to analyze the data for, or 'all' to skip this filter.
    """
    # First check whether we should use week days for filters
    while True:
        filter_type = input(
            'Do you want to [f]ilter the data by week day or use [a]ll week\'s data?\n').lower()
        if filter_type == 'f':
            # If we do, ask for which week day
            while True:
                try:
                    user_day = int(input(
                        'Which week day should we use (1 - Monday, ..., 6 - Saturday, 7 - Sunday)?\n'))
                except ValueError:
                    print("Please, use numbers only.")
                    continue

                if user_day in range(1, 8):
                    week_day = user_day - 1
                    print('You selected "{}", meaning {}. So I will use it in my analysis!'.format(
                        week_day, weekday_name(week_day).capitalize()))
                    break
                else:
                    print('You entered "{}", but it is not a valid option. Please select a  number between 1 and 7.'.format(
                        user_day))
            break
        # Or we use 'all' for not using filters
        elif filter_type == 'a':
            week_day = WEEKDAYS_ALL
            print(
                'Fine, I will not use any filters for week days. We will use all week\'s data')
            break
        else:
            print('You entered "{}", but it is not a valid option. Please select a valid option as shown.'.format(
                filter_type))
            continue

    return week_day


# Loading data

def load_data(city):
    """
    Loads data for a given city.

    Args:
        (str) city - name of the city to analyze

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour_of_day'] = df['Start Time'].dt.hour

    return df


def apply_filters(df, city, month, day):
    """
    Apply filters to a given city.

    Args:
        (dataframe) df - Pandas DataFrame containing city data (non filtered)
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or -1 to apply no month filter
        (str) day - name of the day of week to filter by, or -1 to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df_origin = df

    # filter by month if applicable
    if month != MONTHS_ALL:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != WEEKDAYS_ALL:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    # Print out summary of the data set
    summarize(df_origin, df, city, month, day)

    return df


def summarize(original_df, filtered_df, city, month, day):
    """
    Apply filters to a given city.

    Args:
        (dataframe) original_df - Pandas DataFrame containing city data (non filtered)
        (dataframe) filtered_df - Pandas DataFrame containing city data (filtered)
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or -1 to apply no month filter
        (str) day - name of the day of week to filter by, or -1 to apply no day filter
    """
    print('-'*40)
    print('  Creating statistics for {}'.format(city.capitalize()))

    if month != MONTHS_ALL:
        print('  - Selected month(s): {}'.format(month_name(month).capitalize()))
    else:
        print('  - Selected month(s): All, filters for months are not used')

    if day != WEEKDAYS_ALL:
        print('  - Selected week day(s) -> {}'.format(weekday_name(day).capitalize()))
    else:
        print('  - Selected week day(s) -> All, filters for week days are not used')

    print('  - Number of rides in the original data set: {}'.format(len(original_df)))

    if month != MONTHS_ALL or day != WEEKDAYS_ALL:
        print('  Number of rides in the filtered data set: {}'.format(len(filtered_df)))
    print('-'*40)

# Calculations


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # DONE: display the most common month
    popular_month = df['month'].mode()[0]
    print('  - Most common month of the travel: {}'.format(month_name(popular_month)))

    # DONE: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('  - Most common day of the travel: {}'.format(weekday_name(popular_day)))

    # DONE: display the most common start hour
    popular_hour = df['hour_of_day'].mode()[0]
    print('  - Start hour: {}'.format(format_hour(popular_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    all_rides = len(df)

    # DONE: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_rides = df['Start Station'].value_counts()[
        popular_start_station]
    popular_start_station_rides_per = (
        popular_start_station_rides / all_rides) * 100
    print('  - Start station: {} had {} rides out of {} (hence {:.2f}% of total rides)'
          .format(popular_start_station,
                  popular_start_station_rides,
                  all_rides,
                  popular_start_station_rides_per))

    # DONE: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_rides = df['End Station'].value_counts()[
        popular_end_station]
    popular_end_station_rides_per = (
        popular_end_station_rides / all_rides) * 100
    print('  - End station: {} had {} rides out of {} (hence {:.2f}% of total rides)'
          .format(popular_end_station,
                  popular_end_station_rides,
                  all_rides,
                  popular_end_station_rides_per))

    # DONE: display most frequent combination of start station and end station trip
    df_start_end_stations = df.groupby(['Start Station', 'End Station'])[
        'Start Time'].size().nlargest(1)

    print('  - The most popular trip is from {} to {} with {} rides'
          .format(df_start_end_stations.index.values[0][0],
                  df_start_end_stations.index.values[0][1],
                  df_start_end_stations[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # DONE: display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('  - Total trip duration time is {}'.format(format_seconds(total_travel_time)))

    # DONE: display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('  - Mean trip duration time is {}'.format(format_seconds(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    all_users = len(df)

    # DONE: Display counts of user types
    print('  - User types:')
    user_types = df['User Type'].value_counts()
    for type in range(len(user_types)):
        user_type = user_types.index[type]
        type_value = user_types[type]
        type_percent = (type_value / all_users) * 100
        print('    - {}, number of users of this type: {} ({:.2f}%)'.format(user_type,
                                                                            type_value,
                                                                            type_percent))

    # DONE: Display counts of gender
    # Washington does not have such column, so we need to check for it
    if 'Gender' in df.columns:
        print('  - User genders:')
        user_gendres = df['Gender'].value_counts()
        for gender in range(len(user_gendres)):
            user_gender = user_gendres.index[gender]
            gender_value = user_gendres[gender]
            gender_percent = (gender_value / all_users) * 100
            print('    - {}, number of users of this gender: {} ({:.2f}%)'.format(
                user_gender,
                gender_value,
                gender_percent))

    # DONE: Display earliest, most recent, and most common year of birth
    # Washington does not have such column, so we need to check for it
    if 'Birth Year' in df.columns:
        print('  - User birth statistics:')
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].value_counts().idxmax())

        print('    - The earliest year of birth is {} (good for that person!)'.format(earliest_yob))
        print('    - The most recent year of birth is {}'.format(most_recent_yob))
        print('    - The most common year of birth is {}'.format(most_common_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city)
        df = apply_filters(df, city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
