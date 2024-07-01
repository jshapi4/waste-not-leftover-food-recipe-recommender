import pandas as pd
import streamlit as st
import time


def load_and_preprocess_data(file_path, sample_size):
    # Load the dataset from CSV file
    # sample ONLY
    fdcdf = pd.read_csv(file_path)
    # full data
    # recipe_data = fdcdf

    # Rename columns for consistency
    fdcdf.rename(columns={'id': 'Recipe ID', 'name': 'Recipe Name', 'ingredients': 'Ingredients', 'steps': 'Steps',
                          'description': 'Description'}, inplace=True)

    # Sample a subset of the DataFrame for development
    recipe_data = fdcdf.sample(n=sample_size, random_state=42)

    # Clean ingredients
    recipe_data['Ingredients'] = recipe_data['Ingredients'].apply(clean_ingredients)

    return recipe_data


def clean_ingredients(ingredients_str):
    return ingredients_str.lower().replace('[', '').replace('  ', ' ').replace(']', '').replace('\'', '').split(', ')

# Use st.cache_data to cache the result of this function
@st.cache_data(show_spinner=False)
def cached_load_and_preprocess_data(file_path, sample_size):
    return load_and_preprocess_data(file_path, sample_size)
