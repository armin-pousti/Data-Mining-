#Written by Armin Pousti, and Dmitrii Vlasov
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

"""All the data is gathered from the CovidTimeLineCanada Github which is continually being updated with following 
citation: Berry, I., O’Neill, M., Sturrock, S. L., Wright, J. E., Acharya, K., Brankston, G., Harish, V., Kornas, K., 
Maani, N., Naganathan, T., Obress, L., Rossi, T., Simmons, A. E., Van Camp, M., Xie, X., Tuite, A. R., Greer, A. L., 
Fisman, D. N., & Soucy, J.-P. R. (2021). A sub-national real-time epidemiological and vaccination database for the 
COVID-19 pandemic in Canada. Scientific Data, 8(1). doi: https://doi.org/10.1038/s41597-021-00955-2 """

def preprocessing():
        """
    Preprocessing retrieves data on deaths, cases, completed tests, and hospitalization for COVID-19in Canada from an
    API endpoint. It creates a data frame for each of the data sets, and after cleansing the individual data frames
    from unnecessary columns, it merges all the data frames to create a huge data frame containing all the necessary
    information on COVID19 data.
    :return: <class 'pandas.core.frame.DataFrame'> Returns the processed DataFrame (df_combined)
    """
    # Creating a DataFrame for completed tests for COVID19 in Canada
    completedTest_url = "https://api.opencovid.ca/timeseries?stat=tests_completed&geo=can&fill=false&version=true&pt_names=short&hr_names=hruid&legacy=false&fmt=csv"
    response = requests.get(completedTest_url)
    # converting the byte format into String using the UTF-8 formating
    data1 = response.content.decode("utf-8")
    # converting the CSV string to a file and passing it to the pandas read function
    df_completedTest = pd.read_csv(io.StringIO(data1))
    # removing the region column
    df_completedTest = df_completedTest.drop(["region"], axis=1)

    # Creating a DataFrame for cases for COVID19 in Canada
    cases_url = "https://api.opencovid.ca/timeseries?stat=cases&geo=can&fill=false&version=true&pt_names=short&hr_names=hruid&legacy=false&fmt=csv"
    response = requests.get(cases_url)
    # converting the byte format into String using the UTF-8 formating
    data2 = response.content.decode("utf-8")
    # converting the CSV string to a file and passing it to the pandas read function
    df_cases = pd.read_csv(io.StringIO(data2))
    # removing the region column
    df_cases = df_cases.drop(["region"], axis=1)

    # Creating a DataFrame for deaths for COVID19 in Canada
    deaths_url = "https://api.opencovid.ca/timeseries?stat=deaths&geo=can&fill=false&version=true&pt_names=short&hr_names=hruid&legacy=false&fmt=csv"
    response = requests.get(deaths_url)
    # converting the byte format into String using the UTF-8 formating
    data3 = response.content.decode("utf-8")
    # converting the CSV string to a file and passing it to the pandas read function
    df_deaths = pd.read_csv(io.StringIO(data3))
    # removing the region column
    df_deaths = df_deaths.drop(["region"], axis=1)

    # Creating a DataFrame for hospitalizations for COVID19 in Canada
    hospitalizations_url = "https://api.opencovid.ca/timeseries?stat=hospitalizations&geo=can&fill=false&version=true&pt_names=short&hr_names=hruid&legacy=false&fmt=csv"
    response = requests.get(hospitalizations_url)
    # converting the byte format into String using the UTF-8 formating
    data4 = response.content.decode("utf-8")
    # converting the CSV string to a file and passing it to the pandas read function
    df_hospitalization = pd.read_csv(io.StringIO(data4))
    # removing the region column
    df_hospitalization = df_hospitalization.drop(["region"], axis=1)

    # Creating a new data frame (df) by combining all the DataFrames using the date
    df_combined = pd.merge(df_completedTest, df_cases, on="date", how="inner", suffixes=('_completedTest', '_cases'))
    df_combined = pd.merge(df_combined, df_deaths, on="date", how="inner", suffixes=('_combined', '_deaths'))
    df_combined = pd.merge(df_combined, df_hospitalization, on="date", how="inner",
                           suffixes=('_combined', '_hospitalization'))

    # renaming columns
    df_combined.rename(
        columns={'value_completedTest': 'total_completedTest', 'value_daily_completedTest': 'daily_completedTest',
                 'value_cases': 'total_cases',
                 'value_daily_cases': 'daily_cases', 'value_combined': 'total_deaths',
                 'value_daily_combined': 'daily_deaths',
                 'value_hospitalization': 'total_hospitalization',
                 'value_daily_hospitalization': 'daily_hospitalization'}, inplace=True)
    # removing unnecessary columns
    df_combined = df_combined.drop(['name_completedTest', 'name_cases', 'name_combined', 'name_hospitalization'],
                                   axis=1)

    # to save the processed data csv as an excel file uncomment the next line
    #df_combined.to_excel('processed_data.xlsx')
    return df_combined


#exploratory data analysis analyzes datasets to summarize their main characteristics using statistical graphics
def perform_EDA(data_frame):
    """
    This function performs Exploratory Data Analysis (EDA) on a given data frame. It calculates the data frame's
    summary statistics, including metrics such as count, mean, standard deviation, minimum, quartiles, and maximum
    values for each numeric column. Prints the summary Statistics and returns it as a data frame. The user can save
    it as an Excel file as well.
    :param data_frame: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :return: It does not return anything, and will just plot the EDA on the graph
    """
    #describe() calculates and displays the summary statistics 
    summary_stats = data_frame.describe()
    print("Summary Statistics:\n", summary_stats)
    # to save the summary stats as an excel file uncomment the next line
    #summary_stats.to_excel('SummaryStats_data.xlsx')
    # Line plot for each numeric column
    numeric_cols = data_frame.select_dtypes(include='number').columns

    plt.figure(figsize=(10, 5))
    for col in numeric_cols:
        plt.plot(data_frame.index, data_frame[col], label=col)

    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Line Plot for Numeric Columns')
    plt.legend()
    plt.grid(True)
    plt.show()

    #return summary_stats


def stats_daily_plot(data_frame):
    """
    This function creates a line plot to compare the daily cases, deaths, and completed tests from a given data frame
    over time.
    :param data_frame: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :return: It does not return anything, and will just plot the daily stats graph
    """
    plt.figure(figsize=[15, 8])
    # Convert 'date' column to datetime object
    data_frame['date'] = pd.to_datetime(data_frame['date'])

    plt.plot(data_frame['date'], data_frame['daily_cases'], label='Daily Cases', linewidth = '0.75')
    plt.plot(data_frame['date'], data_frame['daily_deaths'], label='Daily Deaths', linewidth = '0.75')
    plt.plot(data_frame['date'], data_frame['daily_completedTest'], label='Daily Completed Tests', linewidth = '0.75')

    plt.xlabel('Date', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.ylabel('Number of People', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.title('Comparison of Daily Cases, Completed Tests, Deaths, and Hospitalization over Time' , 
    fontdict ={
        'family': 'serif',
        'color':  'xkcd:dark red',
        'weight': 'bold',
        'size': 20,
    },
    loc='left',
    pad=10)
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', alpha=0.5)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Set x-axis to display every month
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format date as 'YYYY-MM-DD'
    plt.xlim(data_frame['date'].min(), pd.to_datetime('2023-01-01')) #not looking at any date later than 2023-01-01 since all plots go down to zero

    plt.tight_layout()
    plt.show()
    #return data_frame


def stats_total_plot(data_frame):
    """
    This function creates a line plot to compare the total cases, deaths, and completed tests from a given data frame
    over time.
    :param data_frame: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :return: It does not return anything, and will just plot the total stats graph
    """
    plt.figure(figsize=[15, 8])
    # Convert 'date' column to datetime object
    data_frame['date'] = pd.to_datetime(data_frame['date'])

    plt.plot(data_frame['date'], data_frame['total_cases'], label='Total Cases', linewidth = '0.75')
    plt.plot(data_frame['date'], data_frame['total_deaths'], label='Total Deaths', linewidth = '0.75')
    plt.plot(data_frame['date'], data_frame['total_completedTest'], label='Total Completed Tests', linewidth = '0.75')

    plt.xlabel('Date', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.ylabel('Number of People', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.title('Comparison of Total Cases, Completed Tests, Deaths, and Hospitalization over Time' , 
    fontdict ={
        'family': 'serif',
        'color':  'xkcd:dark red',
        'weight': 'bold',
        'size': 20,
    },
    loc='left',
    pad=10)
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', alpha=0.5)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Set x-axis to display every month
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format date as 'YYYY-MM-DD'
    plt.tight_layout()
    plt.show()
    #return data_frame


def trend_analysis(df, variable):
    """
    The function calculates and displays the trend of the specified variable over time by plotting the daily values and
    a 7-day rolling average
    :param df: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :param variable: <String> Daily/total cases, deaths, completed tests, and hospitalization for the column to analyze
    :return: It does not return anything, and will just plot the daily tren analysis graphs
    """
    # Convert the date column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Set the date column as the index
    df.set_index('date', inplace=True)
    
    # Calculate the rolling average for the specified variable
    rolling_avg = df[variable].rolling(window=7).mean()
    
    # Plot the trend line
    plt.figure(figsize=(15, 8))
    plt.plot(df.index, df[variable], label='Daily ' + variable, linewidth = '0.75')
    plt.plot(df.index, rolling_avg, label='7-day Rolling Average')
    plt.xlabel('Date', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.ylabel(variable, fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.title('Trend Analysis - ' + variable, 
    fontdict ={
        'family': 'serif',
        'color':  'xkcd:dark red',
        'weight': 'bold',
        'size': 20,
    },
    loc='left',
    pad=10)
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    

def correlation_analysis(df):
    """
    The function visually represents the correlation between numeric variables in the data frame
    :param df: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :return: It does not return anything, and will just plot the daily trend analysis graphs
    """
    # Selecting only columns with numerical values in them
    numeric_df = df.select_dtypes(include='number')
    
    # Compute the correlation matrix which measures the pairwise correlations between the columns of the data frame
    correlation_matrix = numeric_df.corr()
    
    # Generate a heatmap of the correlation matrix
    plt.figure(figsize=(10, 8))
    #creating a heatmap plot of the correlation matrix using the seaborn library
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Analysis', 
    fontdict ={
        'family': 'serif',
        'color':  'xkcd:dark red',
        'weight': 'bold',
        'size': 20,
    },
    loc='left',
    pad=10)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.yticks(rotation=0)  # Keep y-axis labels horizontal
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
    
    

#Written by Armin Pousti, and Dmitrii Vlasov
def cluster_analysis(df, num_clusters):
    """
    Applies K-means clustering to the numeric columns of the DataFrame, grouping similar data points into clusters.
    :param df: <class 'pandas.core.frame.DataFrame'> The processed DataFrame on COVID19 data
    :param num_clusters: <int> for the user to indicate the number of clusters
    :return: <class 'pandas.core.frame.DataFrame'> COVID19 processed DataFrame with the addition of 'Cluster' column
    """
    # Select only the numeric columns from the data frame
    numeric_df = df.select_dtypes(include='number')
    
    # Perform K-means clustering with explicit n_init setting
    kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)  # Set n_init to the desired value
    kmeans.fit(numeric_df)
    
    # Assign cluster labels to each data point
    cluster_labels = kmeans.labels_
    
    # Add a 'Cluster' column to the data frame
    df['Cluster'] = cluster_labels
    

    # Return the data frame with the 'Cluster' column
    return df
def visualize_clusters(df , variable):
    """
    The code helps visualize the clusters obtained from the clustering analysis by plotting the data points on a
    scatter plot, where each point is colored based on its assigned cluster
    :param df: <class 'pandas.core.frame.DataFrame'> COVID19 processed DataFrame with the addition of 'Cluster' column
    :param variable: <String> Daily/total cases, deaths, completed tests, and hospitalization for the column to analyze
    :return: It does not return anything, and will just plot the cluster analysis graphs
    """
    # Convert 'date' column to datetime data type
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract the 'Cluster' column
    clusters = df['Cluster']
    
    # Plot the clusters using a scatter plot
    plt.figure(figsize=(15, 8))
    plt.scatter(df['date'], df[variable], c=clusters, cmap='viridis', s=5)  # Adjust the 's' parameter for smaller points
    plt.xlabel('Date', fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.ylabel(variable, fontdict ={
        'family': 'serif',
        'color':  'xkcd:black',
        'weight': 'normal',
        'size': 16,
    },
    labelpad=8
    )
    plt.title('COVID Cluster Analysis for' + variable,
    fontdict ={
        'family': 'serif',
        'color':  'xkcd:dark red',
        'weight': 'bold',
        'size': 20,
    },
    loc='left',
    pad=10)
    plt.colorbar(label='Cluster')
    plt.xticks(rotation=45, ha='right')
    
    # Set x-axis ticks to two-month intervals
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    plt.show()



