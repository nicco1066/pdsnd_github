#open numpy and pandas library
import numpy as np
import pandas as pd
import calendar

#read file data into 3 pandas dataframes
chicago_data=pd.read_csv('chicago.csv')
new_york_data=pd.read_csv('new_york_city.csv')
washington_data=pd.read_csv('washington.csv')

#create a list with all city tables and a tuple with city names
city_list=[chicago_data,new_york_data,washington_data]
city_name=('Chicago','New York City','Washington')

#formatting tables for future operations
def table_time_formatting(city,i):
    city['Start Time']= pd.to_datetime(city['Start Time'])
    city['Month']= city['Start Time'].dt.month
    #city['Month']= calendar.month_name[city['Month Num']]
    city['Day']=city['Start Time'].dt.dayofweek
    city['Hour']= city['Start Time'].dt.hour
    city['City']=city_name[i]
    city['Trip Duration']=city['Trip Duration']/60
    city['Trip']="From " + city['Start Station']+" to "+city['End Station']
    return(city)

for i in range(3):
    city_list[i]=table_time_formatting(city_list[i],i)

#create an aggregate table to allow analysis on multiple cities at once
city_aggregate=pd.concat(city_list,sort=True)

def display_raw_data(city):
    print('\n\nDo you want to see raw data? \n[1] Yes\n[0] No')
    raw_decision=int(input('Type the corresponding number here:'))
    raw_line=0
    while raw_decision==True:
        print('\n\n')
        print(city.iloc[raw_line:raw_line+5,:])
        raw_line+=5
        print('\n\nDo you want to see more raw data? \n[1] Yes\n[0] No')
        raw_decision=int(input('Type the corresponding number here:'))


#formula to filter table by month and then call table formula analysis
def city_analysis_month_filter(city,city_to_analyse,month):
    city=city[city['Month']==month]
    city_analysis(city,city_to_analyse)
    return

#formula to filter aggregate table by month and then call aggregate table formula analysis
def city_analysis_total_month_filter(cities,month):
    cities=cities[cities['Month']==month]
    city_analysis_total(cities)

#formula to analyse aggregate table
def city_analysis_total(cities):
    popular_month=cities['Month'].mode()[0]
    groupby_tab=cities.groupby(['City'])
    popular_month_by_city=groupby_tab['Month'].apply(lambda x: x.mode().iloc[0])
    popular_day=cities['Day'].mode()[0]
    popular_day_by_city=groupby_tab['Day'].apply(lambda x: x.mode().iloc[0])
    popular_hour=cities['Hour'].mode()[0]
    popular_hour_by_city=groupby_tab['Hour'].apply(lambda x: x.mode().iloc[0])
    popular_start=cities['Start Station'].mode()[0]
    popular_start_by_city=groupby_tab['Start Station'].apply(lambda x: x.mode().iloc[0])
    popular_end=cities['End Station'].mode()[0]
    popular_end_by_city=groupby_tab['End Station'].apply(lambda x: x.mode().iloc[0])
    popular_trip=cities['Trip'].mode()[0]
    popular_trip_by_city=groupby_tab['Trip'].apply(lambda x: x.mode().iloc[0])
    total_travel=cities['Trip Duration'].sum()
    total_travel_by_city=groupby_tab['Trip Duration'].sum()
    avg_travel=cities['Trip Duration'].mean()
    avg_travel_by_city=groupby_tab['Trip Duration'].mean()
    user_type_count=cities['User Type'].value_counts()
    user_type_count_by_city=groupby_tab['User Type'].value_counts()
    print('\n\nMost popular month: {} \nDetail by city (month as number):\n {} '.format(calendar.month_name[popular_month],popular_month_by_city))
    print('\n\nMost popular day of week: {} \nDetail by city (day of week as number 1=Monday, 7=Sunday):\n {} '.format(calendar.month_name[popular_day],popular_day_by_city))
    print('\n\nMost popular hour: {} \nDetail by city:\n {} '.format(popular_hour,popular_hour_by_city))
    print('\n\nMost popular start station: {} \nDetail by city:\n {} '.format(popular_start,popular_start_by_city))
    print('\n\nMost popular end station: {} \nDetail by city:\n {} '.format(popular_end,popular_end_by_city))
    print('\n\nMost popular trip: {} \nDetail by city:\n {} '.format(popular_trip,popular_trip_by_city))
    print('\n\nTotal travel time across cities: {} hour\nDetail by city (in minutes):\n {} '.format(round(total_travel/60,1),total_travel_by_city))
    print('\n\nAverage travel time across cities: {} hour\nDetail by city (in minutes):\n {} '.format(round(avg_travel,1),avg_travel_by_city))
    print('\n\nUser type count across cities: \n{} \nDetail by city:\n {}'.format(user_type_count,user_type_count_by_city))
    display_raw_data(cities)

#formula to analyse single table
def city_analysis(city,city_to_analyse):
    popular_month=city['Month'].mode()[0]
    popular_day=city['Day'].mode()[0]
    popular_hour=city['Hour'].mode()[0]
    popular_start=city['Start Station'].mode()[0]
    popular_end=city['End Station'].mode()[0]
    popular_trip=city['Trip'].mode()[0]
    total_travel=city['Trip Duration'].sum()
    avg_travel=city['Trip Duration'].mean()
    user_type_count=city['User Type'].value_counts()

    print('\n\nHere the data about {}:'.format(city_name[city_to_analyse]))
    print('\n\nMost popular month: {} \nMost popular day: {} \nMost popular hour of day: {}'.format(calendar.month_name[popular_month],calendar.day_name[popular_day],popular_hour))
    print('\n\nMost popular start station: {} \nMost popular end station: {} \nMost popular trip: {}'.format(popular_start,popular_end,popular_trip))
    print('\n\nTotal travel time in the city: {} hour\nAverage travel time: {} minutes'.format(round(total_travel/60,1),round(avg_travel,1)))
    print('\n\nUser type count: \n{}'.format(user_type_count))

    #if for add gender and birth year data in chicago and NYC analysis
    if city_name[city_to_analyse] in ('Chicago','New York City'):
        gender_count=city['Gender'].dropna().value_counts()
        most_common_year=city['Birth Year'].dropna().mode()[0]
        earliest_year=city['Birth Year'].dropna().min()
        most_recent_year=city['Birth Year'].dropna().max()
        print('\n\nGender count:\n{}\n\nMost common year of birth: {}\nEarliest year of birth: {}\nMost recent year of birth: {}\n'.format(gender_count,int(most_common_year),int(earliest_year),int(most_recent_year)))
    display_raw_data(city)


#welcome message
print('\n\nWelcome to Motivate data analysis tool.\n\n')
run_program=True

#While keep the program open until choosen differently
while run_program==True:
    #menu first level
    print('Choose the operation you want to perform by typing the corresponding number:')
    print('[1] Analyse data by city \n[2] Analyse data across cities by time \n[3] Close the program')
    first_operation=int(input('Type the corresponding number here:'))
    if first_operation==1:
        #choose city that you want to analyze
        print('Which city do you want analyse? \n[1] Chicago\n[2] New York City \n[3] Washington')
        city_to_analyse=int(input('Type the corresponding number here:'))-1
        #choose if you want to analyse by month
        print('Do you want to filter data by month?\n[0] No \n[1] Yes')
        month_filter=int(input('Type the corresponding number here:'))
        if month_filter==False:
            city_analysis(city_list[city_to_analyse],city_to_analyse)
        else:
            #choose month you want analyse
            print('Which month do you want to analyse?\n[1] January\n[2] February\n[3] March\n[4] April\n[5] May\n[6] June')
            month=int(input('Type the corresponding number here:'))
            city_analysis_month_filter(city_list[city_to_analyse],city_to_analyse,month)

    if first_operation==2:
        #choose if you want to analyse by month
        print('Do you want to filter data by month?\n[0] No \n[1] Yes')
        month_filter=int(input('Type the corresponding number here:'))
        if month_filter==False:
            city_analysis_total(city_aggregate)
        else:
            #choose month you want analyse
            print('Which month do you want to analyse?\n[1] January\n[2] February\n[3] March\n[4] April\n[5] May\n[6] June')
            month=int(input('Type the corresponding number here:'))
            city_analysis_total_month_filter(city_aggregate,month)

    if first_operation==3:
        run_program=False
    else:
        print('Action not recognized, please input one of number suggested')
