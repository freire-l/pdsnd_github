import time
import pandas as pd
import numpy as np

"""
    Summary of functions
    
    get_filters() - Asks user to specify a city, month, and day to analyze.
    load_data(city, month, day) - Loads data for the specified city and filters by month and day if applicable.
    time_stats(df) - Displays statistics on the most frequent times of travel.
    station_stats(df) - Displays statistics on the most popular stations and trip.
    trip_duration_stats(df) - Displays statistics on the total and average trip duration.
    user_stats(df, city) - Displays statistics on bikeshare users.
    raw_data(df) - Gets raw data if the user wants to see it
    
"""


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    dict_keys = list(CITY_DATA.keys())
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city =  str(input("City to work on: ")).lower()
        if(city in CITY_DATA): 
            break
        else:
            print('Enter a valid city, they are "{}", "{}" and "{}"'.format(dict_keys[0], dict_keys[1], dict_keys[2]))

    # get user input for month (all, january, february, ... , june)
    while True:
        month =  str(input("Month to work on: ")).lower()
        if(month in months): 
            break
        else:
            print('Enter a valid month, they are "{}", "{}", "{}" ... or "{}"'.format(months[0], months[1], months[2], months[-1]))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day =  str(input("Day of the week to work on: ")).title()
        if(day in days):
            break
        else:
            print('Enter a valid day, they are "{}", "{}", "{}" ... or "{}"'.format(days[0], days[1], days[2], days[-1]))

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # Index using weekday int value
        the_day = days.index(day.title())
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == the_day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0] - 1
    print('Most Popular month:', months[month])

    # display the most common day of week
    day = df['day_of_week'].mode()[0] 
    print('Most Popular day:', days[day])

    # display the most common start hour
    print('Most Popular hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % round(time.time() - start_time, 4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common Start Station:', df['Start Station'].mode()[0])
    
    # display most commonly used end station
    print('Most common End  Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    station_comb = ('Start Station: "' + df['Start Station'] + '" End Station: "' + df['End Station'] + '"').mode()[0]
    print('Most Frequent combination of start and end station trip: ', station_comb)

    print("\nThis took %s seconds." % round(time.time() - start_time, 4))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time: ', int(df['Trip Duration'].sum().round()), 'minutes')

    # display mean travel time
    print('Average Travel Time:', round(df['Trip Duration'].mean(), 2) , 'minutes')

    print("\nThis took %s seconds." % round(time.time() - start_time, 4))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n')
    for user, val in user_types.iteritems():
        print (user, val)

    if(city == 'washington'):
        print('\nNo data on gender and year of bith for this filter')
        
    else:
        # Display counts of gender
        user_types = df['Gender'].value_counts()
        print('\nCounts of genders:\n')
        for gender, val in user_types.iteritems():
            print (gender, val)
        
        # Display earliest, most recent, and most common year of birth
        print('Earliest Year of Birth: {} , Most Recent Year of Birth: {}, Most Common Year of bith: {}'.format(int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % round(time.time() - start_time, 4))
    print('-'*40)
    
    
def raw_data(df):
    """Gets raw data if the user wants to see it"""
    curr_row = 0
    
    while True:
        answer =  str(input("Do you want to see the first 5 lines of raw data? yes/no: ")).lower()
        if(restart == 'yes' or restart == 'no'):
            break
        else:
            print('Please enter a valid response\n')


    while True:
        if(answer == 'no'):
            break
        else:
            print(df.iloc[curr_row:curr_row+5,:])
            if(curr_row + 5 >= len(df)):
                print("No more data\n")
                break
            else:
                while True:
                    next =  str(input("Do you want to see the next 5 lines of raw data? yes/no: ")).lower()
                    if(restart == 'yes' or restart == 'no'):
                        break
                    else:
                        print('Please enter a valid response\n')
                if (next == 'yes'):
                    curr_row += 5
                else:
                    break
                


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        while True:
            restart = input('\nWould you like to restart? yes/no\n').lower()
            if(restart == 'yes' or restart == 'no'):
                break
            else:
                print('Please enter a valid response\n')

        if restart == 'no':
            print('-'*40)
            break


if __name__ == "__main__":
	main()
