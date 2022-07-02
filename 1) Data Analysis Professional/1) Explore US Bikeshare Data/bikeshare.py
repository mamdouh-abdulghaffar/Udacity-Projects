import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Whould you like to see data for chicago, new york or washington? \n ").lower()
    while True:
        
        if city not in CITY_DATA:
                print("The city is not in specific cities")
                city = input("Please Enter the city again! \n").lower()
                
        else:
            break
        
    which_filter = input("Would you like to filter the data by month, day, both or not at all? Type 'none' for no time filter.\n ").lower()
    while True:
        if which_filter not in ["month", "day", "both", "none"]:
                which_filter = input("Enter the type of the filter again!!\n ").lower()
        else:
            break

    if which_filter == "none":
        month = "all"
        day   = "all"
    
    if which_filter == "both":
        # get user input for month (all, january, february, ... , june)
        month = input("Which month? January, February, March, April, May or June? \n").lower()
        while True:     
                    
            if month not in ['january', 'february', 'march', 'april', 'june']:
                month = input("Please Enter the month again! \n").lower()
                
            else:
                break              

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = int(input("Which day? Please type your response as an integer (e.g., 1=Sunday) \n"))
        while True:
            
            if day not in range(1, 8):
                day = int(input("Please Enter the day again! \n"))
                
            else:
                break
            
    if which_filter == "month":
        # get user input for month (all, january, february, ... , june)
        month = input("Which month? January, February, March, April, May or June? \n").lower()
        while True:     
                    
            if month not in ['january', 'february', 'march', 'april', 'june']:
                month = input("Please Enter the month again! \n").lower()
                
            else:
                break
            
    if which_filter == "day":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = int(input("Which day? Please type your response as an integer (e.g., 1=Sunday) \n"))
        while True:
            
            if day not in range(1,8):
                day = int(input("Please Enter the day again! \n"))
                
            else:
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
    # load data file into a data frame
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time']   = pd.to_datetime(df['End Time'])
        
    # extract month and day of week from start time to create new columns
    df['month']       = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    # filter by month
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month  = months.index(month) + 1
    
        # filter by month to create the new data frame
        df = df[df['month'] == month] 
        
    # filter by the day of week 
    if day != "all":
        # filter by day of week to create the new data frame
        df = df[df['day_of_week'] == day]           

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nthe most common month is: {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("\nthe most common day of week is: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("\nthe most common start hour is: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most commonly used start station is: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("most commonly used end station is: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("most frequent combination of start station and end station trip is: {}".format(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['travel_time'] = df['End Time'] - df['Start Time']
    
    # display total travel time
    print("total travel time is: {}".format(np.sum(df['travel_time'])))

    # display mean travel time
    print("mean travel time is: {}".format(df['travel_time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("counts of user types is:\n{}\n".format(df['User Type'].value_counts()))

    # Display counts of gender
    if city != "washington":
        print("counts of gender is:\n{}\n".format(df['Gender'].value_counts()))
    
        # Display earliest, most recent, and most common year of birth
        print("earliest year of birth is: {}".format(int(df['Birth Year'].min())))
        print("most recent year of birth is: {}".format(int(df['Birth Year'].max())))
        print("most common year of birth is: {}".format(int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rows(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no? ").lower()
    # check from the validation of view_data
    if view_data == "yes":
        start_loc = 0
        while True:
            print(df.iloc[start_loc:start_loc+5].to_dict('index'), sep= ",")
            start_loc += 5
            view_display = input("\nDo you wish to continue?: ").lower()
            if view_display != "yes":
                break     

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_rows(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
