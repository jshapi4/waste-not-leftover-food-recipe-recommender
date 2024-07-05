import streamlit as st
from data_loader import cached_load_and_preprocess_data
from recipe_finder import find_top_recipes
from utils import *
import time
from pathlib import Path

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

# Load data when needed
recipe_csv = Path(__file__).parents[1] / 'data/food_dot_com_processed_data.csv'
if recipe_data is None:
    recipe_data = cached_load_and_preprocess_data(recipe_csv, 50000)
    # Extract ingredient names from the data for validation
    all_ingredients = set()
    for ingredients in recipe_data['Ingredients']:
        all_ingredients.update(ingredients)
    st.session_state.all_ingredients = all_ingredients


# Function to add ingredient to the list
def add_ingredient():
    ingredient = st.session_state.ingredient_input.strip().lower()
    if ingredient:
        if validate_ingredient(ingredient, st.session_state.all_ingredients):
            if ingredient not in st.session_state.leftover_list:
                st.session_state.leftover_list.append(ingredient)
                st.session_state.ingredient_input = ""
        else:
            ingredient_not_found_warning(ingredient)


# Function to reset the session state
def reset_query():
    st.session_state.leftover_list = []
    st.session_state.show_reset_button = False


# Function to check for results and return a message if there are no matches
def process_recipe_search(recipe_data, leftover_ingredients):
    top_10_recipes, radar_chart_data, top_1000_recipes = find_top_recipes(recipe_data, leftover_ingredients)

    if top_10_recipes is None or top_10_recipes.empty:
        return "Whoops! No recipe ingredients matched your search. Please try adding more ingredients."

    return top_10_recipes, radar_chart_data, top_1000_recipes


# Streamlit app
st.set_page_config(
    page_title="Waste Not: Leftover Ingredients Recipe Finder", # html title
    page_icon="🍽️", # favicon icon
    layout="centered",
    initial_sidebar_state="expanded",
)

# hosted on postimg, this is a banner designed in Canva
banner_url = "https://i.postimg.cc/GpH7Ms1y/waste-not-banner.png"
st.image(banner_url, caption=None, use_column_width=True)
# st.title('Waste Not: Leftover Ingredients Recipe Finder')


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
    if not st.session_state.leftover_list:
        st.warning('Please add some leftover ingredients to the list!')
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Load data when needed
        recipe_csv = Path(__file__).parents[1] / 'data/food_dot_com_processed_data.csv'
        if recipe_data is None: # if recipe data is not loaded into memory, load it:
            recipe_data = cached_load_and_preprocess_data(
                     recipe_csv, 50000
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

        # Process recipe search
        result = process_recipe_search(recipe_data, st.session_state.leftover_list)

        if isinstance(result, str):
            status_text.empty()
            progress_bar.empty()
            st.warning(result)  # Output the message if no recipes matched
        else:
            top_10_recipes, radar_chart_data, top_1000_recipes = result
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


# footer for the bottom of the page
footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: grey;
text-align: center;
}
</style>
<footer class="footer">
<p>&copy; 2024 Joel Shapiro</p>
</footer>
"""
st.markdown(footer,unsafe_allow_html=True)

# Conditionally display the reset button
if st.session_state.show_reset_button:
    if st.button('Reset and search again', type="primary", use_container_width=True):
        reset_query()
        st.rerun()
