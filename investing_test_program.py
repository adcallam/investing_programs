#C++ better performance, but more complicated and difficult for using Machine Learning/AI, plus I am more familiar with Python
#Assess risk and reward of different stocks and allow for comparison
#Note: Yahoo Finance seems to exclude data from weekends as well as possibly holidays and other things like that. 

import matplotlib.pyplot as plt
import numpy as np
import random

import yfinance as yf
import datetime
import pandas as pd
from tqdm import tqdm
import concurrent.futures

def calculate_wait_times(stock_symbol, min_hold_time):
    # Fetch historical stock data
    stock_data = yf.download(stock_symbol, start=None, end=datetime.datetime.today())
    
    # Find the earliest available date in the data
    start_date = stock_data.index.min()
    
    print(f"Earliest available date in the data: {start_date.date()}")
    
    use_earliest_date = input("Do you want to use this as the start date? (y/n): ").strip().lower()
    
    if use_earliest_date == 'n':
        start_date_input = input("Enter your own start date (YYYY-MM-DD): ")
        start_date = pd.Timestamp(start_date_input)
        print("Redownloading data from specified date...")
        stock_data = yf.download(stock_symbol, start=start_date, end=datetime.datetime.today())

    # Convert Pandas to NumPy
    stock_array = stock_data.to_numpy() # Convert DataFrame to NumPy array
    dates = stock_data.index.to_numpy() # Get the dates as a NumPy array

    # Initialize variables for wait time calculations
    sum_of_wait_times = 0
    num_wait_times = 0
    max_wait_time = 0
    max_wait_start_date = None
    max_wait_end_date = None

    total_iterations = len(stock_data)

    # Create a tqdm progress bar
    with tqdm(total=total_iterations, desc="Calculating wait times", unit="iteration") as pbar:
        # Loop through all possible purchase dates
        for i in range(len(stock_array)):

            purchase_price = (stock_array[i,1] + stock_array[i,2]) / 2 # Average of High and Low prices on purchase date
            
            # Calculate profit wait time for each day
            for j in range(len(stock_array)):
                # Skip over dates in the past that have already been analzyed
                if i >= j:
                    continue
                
                if (min_hold_time>(dates[j] - dates[i]).astype('timedelta64[D]').astype(int)):
                    continue

                # Find the first future price greater than or equal to purchase price
                future_price = (stock_array[j,1] + stock_array[j,2]) / 2 # Avergae of High and Low prices on date "j"
                if(future_price<=purchase_price):
                    continue

                wait_time = (dates[j] - dates[i]).astype('timedelta64[D]').astype(int) - min_hold_time
                sum_of_wait_times += wait_time
                num_wait_times+=1
                
                # Update max_wait_time and corresponding dates if applicable
                if wait_time > max_wait_time:
                    max_wait_time = wait_time
                    max_wait_start_date = dates[i]
                    max_wait_end_date = dates[j]
                
                wait_time = 0

                break
            
            pbar.update(1)

    # Calculate the average wait time
    if sum_of_wait_times>0:
        average_wait_time = round(sum_of_wait_times / num_wait_times)
        return average_wait_time, max_wait_time, max_wait_start_date, max_wait_end_date
    else:
        return None, None, None, None

if __name__ == "__main__":
    stock_symbol = input("Enter the stock symbol: ")
    min_hold_time = int(input("Enter your minimum time (days) that you would hold the stock: "))
    print("Downloading stock data...")
    average_wait_time, max_wait_time, max_wait_start_date, max_wait_end_date = calculate_wait_times(stock_symbol, min_hold_time)
    
    if average_wait_time is not None:
        print(f"Average wait time for making a profit (across all possible purchase dates): {average_wait_time} days")
        
        if max_wait_time > 0:
            print(f"Maximum wait time encountered: {max_wait_time} days (from {max_wait_start_date.astype('datetime64[D]')} to {max_wait_end_date.astype('datetime64[D]')})")
    else:
        print("No data available for the given stock.")