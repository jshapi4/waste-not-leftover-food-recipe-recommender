import pandas as pd
import streamlit as st


def load_and_preprocess_data(file_path, sample_size):
    # Load the dataset from CSV file
    fdcdf = pd.read_csv(file_path)

    # Rename columns for consistency
    fdcdf.rename(columns={'id': 'Recipe ID', 'name': 'Recipe Name', 'ingredients': 'Ingredients', 'steps': 'Steps',
                          'description': 'Description'}, inplace=True)

    # Sample a subset of the DataFrame due to processing power limitations
    recipe_data = fdcdf.sample(n=sample_size, random_state=42)

    # Clean ingredients
    recipe_data['Ingredients'] = recipe_data['Ingredients'].apply(clean_ingredients)

    return recipe_data


def clean_ingredients(ingredients_str):
    return ingredients_str.lower().replace('[', '').replace('  ', ' ').replace(']', '').replace('\'', '').split(', ')

# Use st.cache_data to cache the result of this function for increased speed
@st.cache_data(show_spinner=False)
def cached_load_and_preprocess_data(file_path, sample_size):
    return load_and_preprocess_data(file_path, sample_size)
