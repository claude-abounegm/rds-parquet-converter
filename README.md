# rds-parquet-converter

## Parquet to CSV and SQL Converter

This project contains a script to convert Parquet files in a specified directory to both CSV files and SQL `INSERT` statements. Each CSV and SQL file is generated for each parent directory containing Parquet files and is saved in an output directory.

## Background

This project was fully generated by **ChatGPT 4o**. As I was working with an Aurora RDS database, I needed to restore a portion of data from a few tables in RDS. 

To achieve such task, my options were to either:

  1. Restore a full snapshot, which would create a new cluster with the snapshot data -- that is not ideal. I only wanted a very small subset of the data.
  2. Use AWS Athena to process and query the data, but setting up the definitions and putting the pieces together required more work than I was willing to put into for this task.
  3. Export snapshot data to S3 and use that data as needed. Luckily RDS allows us to export specific tables without needing to export the whole snapshot.

With the proper tool, **Option #3** was the fastest, and most feasible option. RDS exports the tables to S3 with the `.parquet.gz` format. Those files are chunked. 
One schema can constitute of many tables, and each table can constitute of many Parquet files, and since S3 does not allow downloading directories, we need to first download the whole S3 directory locally using CLI. This can be done using the `download-s3.sh` script (make sure you have your credentials setup). The script will download the directory into `db-files` directory.

Once the files were downloaded locally, I used ChatGPT to put together a script that generated a CSV file for each `.parquet.gz` file. The next iteration was to name the files properly. The iteration after was to combine all related data into one file. The final iteration was to generate `INSERT` queries. The last prompt was to generate this `README` file. Pretty impressive performance, given that the code generated by ChatGPT was functional on every iteration, with no syntax errors, and produced the exact, expected outcome every time.

## Prerequisites

- Python 3.6+
- pip
- AWS CLI

## Setup

1. **Clone the repository**:
    ```bash
    git clone git@github.com:claude-abounegm/rds-parquet-converter.git
    cd rds-parquet-converter
    ```

2. **Create and activate a virtual environment**:
    ```bash
    ./init-env.sh
    ```

## Usage

1. **Place your Parquet files** in the `db-files/` directory. The directory structure should look something like this:
    ```
    db-files/
    └── .../
        └── schema.table/
            └── subdirectory/
                └── your_file_1.parquet
                └── ...
                └── your_file_N.parquet
    ```

2. **Run the conversion script**:
    ```bash
    ./convert.sh
    ```

    This will read all Parquet files, concatenate them for each parent directory, and save the resulting CSV and SQL files in the `out` directory.

3. **Check the output directory** for the generated CSV and SQL files:
    ```
    out/
    └── schema.table.csv
    └── schema.table.sql
    ```

## Script Explanation

### convert.py

This script performs the following steps:
1. **Identify all unique parent directories** containing Parquet files within the base path (`./db-files`).
2. **Process each parent directory**:
   - Read each Parquet file.
   - Concatenate all DataFrames from the Parquet files into a single DataFrame.
   - Save the combined DataFrame to a CSV file named after the parent directory in the `./out` directory.
   - Generate SQL `INSERT` statements for each row in the DataFrame and save them to a SQL file named after the parent directory in the `./out` directory.
