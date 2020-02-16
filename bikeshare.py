import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_ID = { 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    user_input_city = input('For what city would you like to get the data?\nWe got them streets of Chicago, New York City, even Washington! ').lower()

    while True:
        if user_input_city not in CITY_DATA:
            print('That city is not yet in our database! ')
            user_input_city = input('Maybe try again? ').lower()
        else:
            city = user_input_city
            print('Showing data for:', user_input_city.title())
            print('Great choice!')
            break

    user_input_month = input('Moving on, for what month would you like to see data?\nAll, or for a specific month (January to June)? ').lower()

    while True:
        if user_input_month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print('That\'s not a real month, mom! ')
            user_input_month = input('Maybe try again? ').lower()
        else:
                month = user_input_month
                print('Showing data for:', user_input_month.title())
                break

    user_input_day = input('And for what day would the kind sir/madam like to\nfilter the data? All, or a specific day of week? ').lower()

    while True:
        if user_input_day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('That\'s not a real day, mom! ')
            user_input_day = input('Maybe try again? ').lower()
        else:
            day = user_input_day
            print('Showing data for: ', user_input_day.title())
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    if month == 'all':
        print('Loading data for all months..')
    else:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df.loc[df['Month'] == month]

    if day == 'all':
        print('Loading data for all days..')
    else:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df.loc[df['Day_of_week'] == day]

        print('Currently computing along', df.count()[0], 'rows in this database')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df[['Month']].mode().iloc[0][0]
    print('The most common month was: ', popular_month)

    popular_day = df[['Day_of_week']].mode().iloc[0][0]
    print('The most common day of the week was: ', popular_day)
    popular_hour = df[['Hour']].mode().iloc[0][0]
    print('..aaand finally, the most common hour was: ', popular_hour)

    print("\nThis whole operation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', most_common_station)

    most_common_stop = df['Start Station'].value_counts().idxmax()
    print('The most commonly used stop station is: ', most_common_stop)

    most_common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print('The most frequent combination of start and end stations are:', most_common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Total Travel Time'] = pd.to_timedelta(df['End Time']) - pd.to_timedelta(df['Start Time'])
    print('So adding together all trips, we\'d get up to a total time of', total_time.sum())
    df['Total Time'] = df['End Time'] - df['Start Time']
    print('Also, by power of maths, we got up to an average trip time of', df['Total Time'].mean()/60)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df.groupby(['User Type']).count()
    if user_type.shape[0] == 2:
        print('Based on our data, we have', user_type['Start Time'][0], 'Customers, and', user_type['Start Time'][1], 'Subscribers!')
    elif user_type.shape[0] == 3:
        print('Based on our data, we have', user_type['Start Time'][0], 'Customers,', user_type['Start Time'][1], 'Dependents and ', user_type['Start Time'][2], 'Subscribers!')

    if 'Gender' not in df:
        print('We don\'t seem to have any gender data for this city, though - blame GDPR!')
    else:
        gender_type = df.groupby(['Gender']).count()
        print('Based on our data, we have', gender_type['Start Time'][0], 'Female Users, and', gender_type['Start Time'][1], 'Male Users!')

    if 'Birth Year' not in df.columns:
        print('We can\'t show you any data about user birthdays :(, as we don\'t have them stored!')
    else:
        earliest_birthdate = df['Birth Year'].min()
        most_recent_birthdate = df['Birth Year'].max()
        most_common_birthdate = df['Birth Year'].mode()[0]
        print('Hey, we have some birthday data to show as well! The earliest birthdate is for someone born in', earliest_birthdate)
        print('Some more birthday data! Our youngest subscriber is born in', most_recent_birthdate)
        print('Finally, most subscribers are born in', most_common_birthdate)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    raw_data = input('Would you like to see some raw data from our dataframe? Enter yes or no.\n').lower()

    if raw_data == 'yes':
        index = 0
        print(df.iloc[index:index+5])
        carry_on = input('Would you like to see more? Enter yes or no.').lower()
        while carry_on == 'yes':
            index += 5
            print(df.iloc[index:index+5])
            carry_on = input('Would you like to see more? Enter yes or no.').lower()
        else:
            print('Bye bye now!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
