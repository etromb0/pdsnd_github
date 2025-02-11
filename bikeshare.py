import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def validate_city():
    valid_cities = ['chicago', 'new york city', 'washington']
    while True:
        try:
            filteredcity = input('Enter a city: ').lower()
            if filteredcity in valid_cities:
                return filteredcity
                break;
            else:
                print('That\'s not a valid city')
        except:            
            continue
            
def validate_month():
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        try:
            filteredmonth = input('Enter the name of a month from january to june or enter "all": ').lower()
            if filteredmonth in valid_months:
                return filteredmonth
                break;
            else:
                print('That\'s not a valid month')
        except:            
            continue
            
def validate_weekday():
    valid_weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    while True:
        try:
            filteredweekday = input('Enter the name of a day of the week or enter "all": ').lower()
            if filteredweekday in valid_weekdays:
                return filteredweekday
                break;
            else:
                print('That\'s not a valid weekday')
        except:            
            continue     
            
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = validate_city()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = validate_month()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = validate_weekday()
    
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
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month]    
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df
#city, month, day = get_filters()
#df = load_data(city, month, day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)
    
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: ', common_day_of_week)

    # TO DO: display the most common start hour
    start_hour = df['Start Time'].dt.hour
    common_start_hour = start_hour.mode()[0]
    print('The most common start hour is: ', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most common end station is: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    station_combinations = df.groupby(['Start Station', 'End Station']).size()
    most_common = station_combinations.sort_values(ascending=False).head(1)
    print('The most frequent combination of start station and end station is: ', most_common.index[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    travel_time = df['End Time'] - df['Start Time']
    total_travel_time = travel_time.sum()
    print('The total travel time is: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = travel_time.mean()
    print('The average travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df.groupby('User Type')['User Type'].count())
    while True:
        try:
            
    # TO DO: Display counts of gender
            print(df.groupby('Gender')['Gender'].count())
                     
    # TO DO: Display earliest, most recent, and most common year of birth
            print('The earliest birth year is: ', int(df['Birth Year'].min()))
            print('The most recent birth year is: ', int(df['Birth Year'].max()))
            print('The most common birth year is: ', int(df['Birth Year'].mode()))   
        
        except KeyError:
               print('Washington does not have Gender or Birth Year data.')
        break
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_data = input('\nWould you like to see 5 lines of data? Enter yes or no.\n')
        start_loc = 0
        while view_data.lower() == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_display = input('Do you wish to see 5 more lines of data?').lower()
            if view_display == 'no':
                break
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()