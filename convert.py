import pandas as pd
import glob
import os

# Function to get all unique parent directories containing Parquet files
def get_unique_parent_directories(base_path):
    parquet_files = glob.glob(f"{base_path}/**/*.parquet", recursive=True)
    parent_directories = set(os.path.dirname(os.path.dirname(file)) for file in parquet_files)
    return parent_directories

# Function to process Parquet files in a given parent directory and save to CSV
def process_parent_directory(parent_directory, output_directory):
    # Initialize an empty list to hold the DataFrames
    df_list = []

    # Loop through each Parquet file in the parent directory and its subdirectories
    for parquet_file in glob.glob(f"{parent_directory}/**/*.parquet", recursive=True):
        # Read the Parquet file
        df = pd.read_parquet(parquet_file)
        
        # Append the DataFrame to the list
        df_list.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    # Extract the parent directory name for the CSV file
    base_dir_name = os.path.basename(parent_directory)
    csv_file_name = f"{base_dir_name}.csv"

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save the combined DataFrame to a single CSV file in the output directory
    output_path = os.path.join(output_directory, csv_file_name)
    combined_df.to_csv(output_path, index=False)

# Base path containing the Parquet files
base_path = "./db-files"
# Output directory to save the CSV files
output_directory = "./out"

# Get all unique parent directories
parent_directories = get_unique_parent_directories(base_path)

# Process each parent directory
for parent_directory in parent_directories:
    process_parent_directory(parent_directory, output_directory)
