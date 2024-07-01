import streamlit as st
from data_loader import cached_load_and_preprocess_data
from recipe_finder import find_top_recipes
from utils import *
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

if 'rerun_trigger' not in st.session_state:
    st.session_state.rerun_trigger = 0


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
st.set_page_config(
    page_title="Waste Not: Leftover Ingredients Recipe Finder",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="expanded",
)

banner_url = "https://i.postimg.cc/GpH7Ms1y/waste-not-banner.png"
st.image(banner_url, caption=None, use_column_width=True)
st.title('Waste Not: Leftover Ingredients Recipe Finder')


# Form for ingredient input
with st.form(key='ingredient_form'):
    st.header('Enter your leftover ingredients:')
    ingredient = st.text_input('Type an ingredient', key='ingredient_input')
    submit_button = st.form_submit_button(label='Add to list', on_click=add_ingredient)

# Display the current list of ingredients and handle editing
display_ingredients_list(st.session_state.leftover_list)
edit_ingredient_popup()

# Find recipes button and results
if st.button("Find recipes!", type="primary", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()

    if st.session_state.leftover_list:
        # Load data only when needed
        if recipe_data is None:
            recipe_data = cached_load_and_preprocess_data(
                     '/Users/joelshapiro/Documents/WGU/C964/Shapiro_Capstone/data/food_dot_com_processed_data.csv',
                      50000
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
        top_10_recipes, radar_chart_data, top_1000_recipes = find_top_recipes(recipe_data, st.session_state.leftover_list)

        progress_bar.progress(60)

        for i in range(60, 100):
            time.sleep(0.05)
            progress_bar.progress(i)

        progress_bar.progress(100)
        status_text.text('Recipe matching complete!')
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()

        # Display the top 10 with radar charts
        display_top_recipes(top_10_recipes, radar_chart_data)

        # Create an expander for the recipe details
        with st.expander("Supporting Data Visuals", expanded=False):
            # Display Bar Chart below the top 10
            display_top_recipes_similarity_bar_chart(top_10_recipes)
            # 3rd Visualization
            plot_similarity_vs_usage_scatter(top_1000_recipes)

        # Set flag to show reset button
        st.session_state.show_reset_button = True
    else:
        st.warning('Please add some leftover ingredients to the list!')

# Conditionally display the reset button
if st.session_state.show_reset_button:
    if st.button('Reset and search again', type="primary", use_container_width=True):
        reset_query()
        st.rerun()
