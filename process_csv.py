import pandas as pd


def process_csv_with_pandas(input_file, output_file):
    df = pd.read_csv(input_file)

    # Modify specific columns to proper case (e.g., 'column_name')
    #df['name'] = df['name'].str.strip().str.title()
    # Perform search and replace
    df['name'] = df['name'].str.replace(' S ', "'s ")

    df.to_csv(output_file, index=False)
    print(f"Successfully processed {input_file}")
    print(f"Successfully saved {output_file}")


# Process the file to change case
input_filename = './data/food_dot_com_processed.csv'
output_filename = 'data/food_dot_com_processed_data.csv'

process_csv_with_pandas(input_filename, output_filename)