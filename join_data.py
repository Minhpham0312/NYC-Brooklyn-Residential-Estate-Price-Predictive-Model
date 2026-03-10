import pandas as pd
import glob
import os

def merge_brooklyn_housing_data(directory_path='.'):
    # Target years from 2009 to 2023
    years = range(2009, 2023)
    df_list = []
    
    for year in years:
        file_path = os.path.join(directory_path, f"brooklyn_{year}.csv")
        if os.path.exists(file_path):
            print(f"Reading {file_path}...")
            df_list.append(pd.read_csv(file_path))
        else:
            print(f"Warning: File for year {year} not found.")

    if not df_list:
        print("No Brooklyn housing files found for the specified years.")
        return None

    print(f"Merging {len(df_list)} files...")
    merged_df = pd.concat(df_list, ignore_index=True)
    
    return merged_df

if __name__ == "__main__":
    brooklyn_data = merge_brooklyn_housing_data()
    if brooklyn_data is not None:
        print(f"Successfully merged data. Total records: {len(brooklyn_data)}")
        brooklyn_data.to_csv('merged_brooklyn_housing.csv', index=False)
        
        # Read back the exported file to show the data
        reloaded_data = pd.read_csv('merged_brooklyn_housing.csv')
        print("\nPreview of reloaded data:")
        print(reloaded_data.head())