import pandas as pd
import streamlit as st
import time

def load_and_preprocess_data_with_progress(file_path='/Users/joelshapiro/Documents/WGU/C964/Shapiro_Capstone/data/RAW_recipes_Food_com.csv', sample_size=170000):
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Set the maximum number of columns to display
    pd.set_option('display.max_columns', 50)

    # Simulate progress for loading the dataset
    status_text.text('Loading dataset...')
    for i in range(30):
        time.sleep(0.05)
        progress_bar.progress(i)

    # Load the dataset from CSV file
    #fdcdf = pd.read_csv(file_path)
    recipe_data = pd.read_csv(file_path)
    progress_bar.progress(30)

    # Rename columns for consistency
    status_text.text('Preprocessing data...')
    recipe_data.rename(columns={'id': 'Recipe ID', 'name': 'Recipe Name', 'ingredients': 'Ingredients'}, inplace=True)
    for i in range(30, 60):
        time.sleep(0.05)
        progress_bar.progress(i)

    # Sample a subset of the DataFrame for development
    #recipe_data = fdcdf.sample(n=sample_size, random_state=42)
    #recipe_data = fdcdf
    progress_bar.progress(60)

    # Clean ingredients
    status_text.text('Cleaning ingredients...')
    recipe_data['Ingredients'] = recipe_data['Ingredients'].apply(clean_ingredients)
    for i in range(60, 100):
        time.sleep(0.05)
        progress_bar.progress(i)

    progress_bar.progress(100)
    status_text.text('Data loading complete!')
    #time.sleep(1)
    status_text.empty()
    progress_bar.empty()

    return recipe_data

def clean_ingredients(ingredients_str):
    return ingredients_str.lower().replace('[', '').replace('  ', ' ').replace(']', '').replace('\'', '').split(', ')

# Use st.cache_data to cache the result of this function
@st.cache_data(show_spinner=False)
def cached_load_and_preprocess_data(file_path, sample_size):
    return load_and_preprocess_data_with_progress(file_path, sample_size)

def progress_bar():
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.text('Loading results...')
    for i in range(1, 100):
        time.sleep(0.05)
        progress_bar.progress(i)

