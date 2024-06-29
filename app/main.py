import streamlit as st
from data_loader import cached_load_and_preprocess_data
from recipe_finder import find_top_recipes
from utils import display_ingredients_list, display_top_recipes
import time

# Global variable to hold the data
recipe_data = None

# Initialize session state
if 'leftover_list' not in st.session_state:
    st.session_state.leftover_list = []

if 'ingredient_input' not in st.session_state:
    st.session_state.ingredient_input = ""

if 'show_reset_button' not in st.session_state:
    st.session_state.show_reset_button = False

# Function to add ingredient to the list
def add_ingredient():
    if st.session_state.ingredient_input and st.session_state.ingredient_input not in st.session_state.leftover_list:
        st.session_state.leftover_list.append(st.session_state.ingredient_input)
        st.session_state.ingredient_input = ""

# Function to reset the session state
def reset_query():
    st.session_state.leftover_list = []
    st.session_state.show_reset_button = False


# Streamlit app
st.image("./waste-not-logo.png", caption=None, use_column_width=True)
st.title('Waste Not: Leftover Ingredients Recipe Finder')
st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    """, unsafe_allow_html=True)

# Form for ingredient input
with st.form(key='ingredient_form'):
    st.header('Enter your leftover ingredients:')
    ingredient = st.text_input('Type an ingredient', key='ingredient_input')
    submit_button = st.form_submit_button(label='Add to list', on_click=add_ingredient)

# Display the current list of ingredients
display_ingredients_list(st.session_state.leftover_list)

# Find recipes button and results
if st.button("Find recipes!", type="primary", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()

    if st.session_state.leftover_list:
        # Load data only when needed
        if recipe_data is None:
            recipe_data = cached_load_and_preprocess_data(
                '/Users/joelshapiro/Documents/WGU/C964/Shapiro_Capstone/data/RAW_recipes_Food_com.csv',
                1000
            )

        # Simulate progress for loading the dataset
        status_text.text('Loading dataset...')
        for i in range(30):
            time.sleep(0.05)
            progress_bar.progress(i)

        progress_bar.progress(30)
        status_text.text('Processing data...')

        for i in range(30, 60):
            time.sleep(0.05)
            progress_bar.progress(i)

        status_text.text('Calculating the best matches...')

        # Calculate top 10
        top_10_recipes = find_top_recipes(recipe_data, st.session_state.leftover_list)

        progress_bar.progress(60)

        for i in range(60, 100):
            time.sleep(0.05)
            progress_bar.progress(i)

        progress_bar.progress(100)
        status_text.text('Data loading complete!')
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()

        # Display the top 10
        display_top_recipes(top_10_recipes)

        # Set flag to show reset button
        st.session_state.show_reset_button = True
    else:
        st.warning('Please add some leftover ingredients to the list!')

# Conditionally display the reset button
if st.session_state.show_reset_button:
    if st.button('Reset and search again'):
        reset_query()
        st.rerun()