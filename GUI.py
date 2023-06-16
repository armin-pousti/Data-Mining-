#Written by Armin Pousti, and Dmitrii Vlasov
import tkinter as tk
import COVID19

def perform_eda():
    data_frame = COVID19.preprocessing()
    COVID19.perform_EDA(data_frame)

def perform_time_series():
    def handle_time_series_option():
        option = time_series_option.get()
        data_frame = COVID19.preprocessing()
        if option == '1':
            COVID19.stats_daily_plot(data_frame)
        elif option == '2':
            COVID19.stats_total_plot(data_frame)

    time_series_window = tk.Toplevel(main_window)
    time_series_window.title("Time Series")
    time_series_option = tk.StringVar()
    tk.Label(time_series_window, text="Select one of the following options:").pack()
    tk.Radiobutton(time_series_window, text="Daily", variable=time_series_option, value="1").pack()
    tk.Radiobutton(time_series_window, text="Total", variable=time_series_option, value="2").pack()
    tk.Button(time_series_window, text="Select", command=handle_time_series_option).pack()

def perform_trend_analysis():
    def handle_trend_analysis_option():
        ans = trend_analysis_option.get()
        data_frame = COVID19.preprocessing()
        if ans == '1':
            def handle_trend_analysis_dataset():
                ans1 = trend_analysis_dataset_option.get()
                if ans1 == '1':
                    COVID19.trend_analysis(data_frame, 'daily_cases')
                elif ans1 == '2':
                    COVID19.trend_analysis(data_frame, 'daily_deaths')
                elif ans1 == '3':
                    COVID19.trend_analysis(data_frame, 'daily_completedTest')
                elif ans1 == '4':
                    COVID19.trend_analysis(data_frame, 'daily_hospitalization')

            trend_analysis_dataset_window = tk.Toplevel(main_window)
            trend_analysis_dataset_window.title("Trend Analysis - Daily")
            trend_analysis_dataset_option = tk.StringVar()
            tk.Label(trend_analysis_dataset_window, text="Select the data set you want to analyze:").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Daily Cases", variable=trend_analysis_dataset_option, value="1").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Daily Deaths", variable=trend_analysis_dataset_option, value="2").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Daily Completed Tests", variable=trend_analysis_dataset_option, value="3").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Daily Hospitalization", variable=trend_analysis_dataset_option, value="4").pack()
            tk.Button(trend_analysis_dataset_window, text="Select", command=handle_trend_analysis_dataset).pack()
        elif ans == '2':
            def handle_trend_analysis_dataset():
                ans2 = trend_analysis_dataset_option.get()
                if ans2 == '1':
                    COVID19.trend_analysis(data_frame, 'total_cases')
                elif ans2 == '2':
                    COVID19.trend_analysis(data_frame, 'total_deaths')
                elif ans2 == '3':
                    COVID19.trend_analysis(data_frame, 'total_completedTest')
                elif ans2 == '4':
                    COVID19.trend_analysis(data_frame, 'total_hospitalization')

            trend_analysis_dataset_window = tk.Toplevel(main_window)
            trend_analysis_dataset_window.title("Trend Analysis - Total")
            trend_analysis_dataset_option = tk.StringVar()
            tk.Label(trend_analysis_dataset_window, text="Select the data set you want to analyze:").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Total Cases", variable=trend_analysis_dataset_option, value="1").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Total Deaths", variable=trend_analysis_dataset_option, value="2").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Total Completed Tests", variable=trend_analysis_dataset_option, value="3").pack()
            tk.Radiobutton(trend_analysis_dataset_window, text="Total Hospitalization", variable=trend_analysis_dataset_option, value="4").pack()
            tk.Button(trend_analysis_dataset_window, text="Select", command=handle_trend_analysis_dataset).pack()

    trend_analysis_window = tk.Toplevel(main_window)
    trend_analysis_window.title("Trend Analysis")
    trend_analysis_option = tk.StringVar()
    tk.Label(trend_analysis_window, text="Select one of the following options:").pack()
    tk.Radiobutton(trend_analysis_window, text="Daily", variable=trend_analysis_option, value="1").pack()
    tk.Radiobutton(trend_analysis_window, text="Total", variable=trend_analysis_option, value="2").pack()
    tk.Button(trend_analysis_window, text="Select", command=handle_trend_analysis_option).pack()

def perform_correlation_analysis():
    data_frame = COVID19.preprocessing()
    COVID19.correlation_analysis(data_frame)

def perform_cluster_analysis():
    def handle_cluster_analysis():
        number_clusters = cluster_number_entry.get()
        data_frame = COVID19.preprocessing()
        clustered_covid_df = COVID19.cluster_analysis(data_frame, int(number_clusters))

        def handle_visualize_clusters_option():
            ans = visualize_clusters_option.get()
            if ans == '1':
                def handle_visualize_clusters_dataset():
                    ans1 = visualize_clusters_dataset_option.get()
                    if ans1 == '1':
                        COVID19.visualize_clusters(clustered_covid_df, 'daily_cases')
                    elif ans1 == '2':
                        COVID19.visualize_clusters(clustered_covid_df, 'daily_deaths')
                    elif ans1 == '3':
                        COVID19.visualize_clusters(clustered_covid_df, 'daily_completedTest')
                    elif ans1 == '4':
                        COVID19.visualize_clusters(clustered_covid_df, 'daily_hospitalization')

                visualize_clusters_dataset_window = tk.Toplevel(main_window)
                visualize_clusters_dataset_window.title("Visualize Clusters - Daily")
                visualize_clusters_dataset_option = tk.StringVar()
                tk.Label(visualize_clusters_dataset_window, text="Select the data set you want to analyze:").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Daily Cases", variable=visualize_clusters_dataset_option, value="1").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Daily Deaths", variable=visualize_clusters_dataset_option, value="2").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Daily Completed Tests", variable=visualize_clusters_dataset_option, value="3").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Daily Hospitalization", variable=visualize_clusters_dataset_option, value="4").pack()
                tk.Button(visualize_clusters_dataset_window, text="Select", command=handle_visualize_clusters_dataset).pack()
            elif ans == '2':
                def handle_visualize_clusters_dataset():
                    ans2 = visualize_clusters_dataset_option.get()
                    if ans2 == '1':
                        COVID19.visualize_clusters(clustered_covid_df, 'total_cases')
                    elif ans2 == '2':
                        COVID19.visualize_clusters(clustered_covid_df, 'total_deaths')
                    elif ans2 == '3':
                        COVID19.visualize_clusters(clustered_covid_df, 'total_completedTest')
                    elif ans2 == '4':
                        COVID19.visualize_clusters(clustered_covid_df, 'total_hospitalization')

                visualize_clusters_dataset_window = tk.Toplevel(main_window)
                visualize_clusters_dataset_window.title("Visualize Clusters - Total")
                visualize_clusters_dataset_option = tk.StringVar()
                tk.Label(visualize_clusters_dataset_window, text="Select the data set you want to analyze:").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Total Cases", variable=visualize_clusters_dataset_option, value="1").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Total Deaths", variable=visualize_clusters_dataset_option, value="2").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Total Completed Tests", variable=visualize_clusters_dataset_option, value="3").pack()
                tk.Radiobutton(visualize_clusters_dataset_window, text="Total Hospitalization", variable=visualize_clusters_dataset_option, value="4").pack()
                tk.Button(visualize_clusters_dataset_window, text="Select", command=handle_visualize_clusters_dataset).pack()

        visualize_clusters_window = tk.Toplevel(main_window)
        visualize_clusters_window.title("Visualize Clusters")
        visualize_clusters_option = tk.StringVar()
        tk.Label(visualize_clusters_window, text="Select one of the following options:").pack()
        tk.Radiobutton(visualize_clusters_window, text="Daily", variable=visualize_clusters_option, value="1").pack()
        tk.Radiobutton(visualize_clusters_window, text="Total", variable=visualize_clusters_option, value="2").pack()
        tk.Button(visualize_clusters_window, text="Select", command=handle_visualize_clusters_option).pack()

    cluster_analysis_window = tk.Toplevel(main_window)
    cluster_analysis_window.title("Cluster Analysis")
    cluster_number_label = tk.Label(cluster_analysis_window, text="Choose the number of clusters: ")
    cluster_number_label.pack()
    cluster_number_entry = tk.Entry(cluster_analysis_window)
    cluster_number_entry.pack()
    tk.Button(cluster_analysis_window, text="Select", command=handle_cluster_analysis).pack()

# Create the main window
main_window = tk.Tk()
main_window.title("COVID19 Data Mining")
main_window.geometry("400x300")  # Set the window size

# Set the background and foreground colors
main_window.configure(bg="lightgray")

# Create a frame for center alignment
center_frame = tk.Frame(main_window, bg="lightgray")
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create the labels and buttons for the options
tk.Label(center_frame, text="Select one of the following techniques:", font=("Arial", 16), bg="lightgray").pack(pady=10)
tk.Button(center_frame, text="Exploratory Data Analysis", font=("Arial", 12), command=perform_eda).pack(pady=5)
tk.Button(center_frame, text="Time Series", font=("Arial", 12), command=perform_time_series).pack(pady=5)
tk.Button(center_frame, text="Trend Analysis", font=("Arial", 12), command=perform_trend_analysis).pack(pady=5)
tk.Button(center_frame, text="Correlation Analysis", font=("Arial", 12), command=perform_correlation_analysis).pack(pady=5)
tk.Button(center_frame, text="Cluster Analysis", font=("Arial", 12), command=perform_cluster_analysis).pack(pady=5)

# Start the main event loop
main_window.mainloop()