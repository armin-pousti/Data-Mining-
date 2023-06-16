#Written by Armin Pousti, and Dmitrii Vlasov
import COVID19

print("COVID19 Data Mining")
print("Select one of the following techniques:")
print("1) Exploratory Data Analysis")
print("2) Time Series")
print("3) Trend Analysis")
print("4) Correlation Analysis")
print("5) Cluster Analysis")
data_frame = COVID19.preprocessing()

user = input("Option : ")
if user == '1':
    COVID19.perform_EDA(data_frame)
elif user == '2':
    print("Selected one of the following options:")
    print("1) Daily")
    print("2) Total")
    option = input("Option : ")
    if option == '1':
        COVID19.stats_daily_plot(data_frame)
    elif option == '2':
        COVID19.stats_total_plot(data_frame)
elif user == '3':
    print("Selected one of the following options:")
    print("1) Daily")
    print("2) Total")
    ans = input("Option : ")
    if ans == '1':
        print("Select the data set you want to analyze:")
        print("1) Daily Cases")
        print("2) Daily Deaths")
        print("3) Daily Completed Tests")
        print("4) Daily Hospitalization")
        ans1 = input("Option : ")
        if ans1 == '1':
            COVID19.trend_analysis(data_frame, 'daily_cases')
        elif ans1 == '2':
            COVID19.trend_analysis(data_frame, 'daily_deaths')    
        elif ans1 == '3':
            COVID19.trend_analysis(data_frame, 'daily_completedTest')
        elif ans1 == '4':
            COVID19.trend_analysis(data_frame, 'daily_hospitalization')
    elif ans == '2':
        print("Select the data set you want to analyze:")
        print("1) Total Cases")
        print("2) Total Deaths")
        print("3) Total Completed Tests")
        print("4) Total Hospitalization")
        ans2 = input("Option : ")
        if ans2 == '1':
            COVID19.trend_analysis(data_frame, 'total_cases')
        elif ans2 == '2':
            COVID19.trend_analysis(data_frame, 'total_deaths')    
        elif ans2 == '3':
            COVID19.trend_analysis(data_frame, 'total_completedTest')
        elif ans2 == '4':
            COVID19.trend_analysis(data_frame, 'total_hospitalization')

elif user == '4':
        COVID19.correlation_analysis(data_frame)







elif user == '5':
    number_clusters = input("Choose the number of clusters : ")
    clustered_covid_df = COVID19.cluster_analysis(data_frame, int(number_clusters))
    print("Selected one of the following options:")
    print("1) Daily")
    print("2) Total")
    ans = input("Option : ")
    if ans == '1':
        print("Select the data set you want to analyze:")
        print("1) Daily Cases")
        print("2) Daily Deaths")
        print("3) Daily Completed Tests")
        print("4) Daily Hospitalization")
        ans1 = input("Option : ")
        if ans1 == '1':
            #visualize_clusters(clustered_covid_df, 'daily_cases')
            COVID19.visualize_clusters(clustered_covid_df, 'daily_cases')
        elif ans1 == '2':
            COVID19.visualize_clusters(clustered_covid_df, 'daily_deaths')    
        elif ans1 == '3':
            COVID19.visualize_clusters(clustered_covid_df, 'daily_completedTest')
        elif ans1 == '4':
            COVID19.visualize_clusters(clustered_covid_df, 'daily_hospitalization')
    elif ans == '2':
        print("Select the data set you want to analyze:")
        print("1) Total Cases")
        print("2) Total Deaths")
        print("3) Total Completed Tests")
        print("4) Total Hospitalization") 
        ans2 = input("Option : ")
        if ans2 == '1':
            COVID19.visualize_clusters(clustered_covid_df, 'total_cases')
        elif ans2 == '2':
            COVID19.visualize_clusters(clustered_covid_df, 'total_deaths')    
        elif ans2 == '3':
            COVID19.visualize_clusters(clustered_covid_df, 'total_completedTest')
        elif ans2 == '4':
            COVID19.visualize_clusters(clustered_covid_df, 'total_hospitalization')

        
