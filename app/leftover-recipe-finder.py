import streamlit as st
from PIL import Image
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


# Set the maximum number of columns to display
pd.set_option('display.max_columns', 50)

# Load the dataset from CSV file
fdcdf = pd.read_csv('/Users/joelshapiro/Documents/WGU/C964/Shapiro_Capstone/data/RAW_recipes_Food_com.csv')

# Rename columns for consistency
fdcdf.rename(columns={'id': 'Recipe ID', 'name': 'Recipe Name', 'ingredients': 'Ingredients'}, inplace=True)

# Sample a subset of the DataFrame for development
sample_size = 2000  # Small right now to keep the time to run the program shorter
recipe_data = fdcdf.sample(n=sample_size, random_state=42)


# Ensure ingredients are in the correct format
def clean_ingredients(ingredients_str):
    return ingredients_str.lower().replace('[', '').replace('  ', ' ').replace(']', '').replace('\'', '').split(', ')


recipe_data['Ingredients'] = recipe_data['Ingredients'].apply(clean_ingredients)


# Function to calculate the percentage of leftover ingredients used in each recipe
def calculate_leftover_usage(ingredients, leftover_set):
    ingredients_set = set(ingredients)
    intersection = ingredients_set.intersection(leftover_set)
    unused_leftovers = leftover_set.difference(ingredients_set)
    ingredients_to_buy = ingredients_set.difference(leftover_set)
    return len(intersection) / len(leftover_set) * 100, intersection, unused_leftovers, ingredients_to_buy


# Function to process the recipes and find the top 10 matches
def find_top_recipes(leftover_ingredients):
    # Use MultiLabelBinarizer with sparse output to one-hot encode the ingredients
    mlb = MultiLabelBinarizer(sparse_output=True)
    ingredient_matrix = mlb.fit_transform(recipe_data['Ingredients'])
    f_ingredient_names = mlb.classes_

    # Convert to sparse DataFrame
    recipe_ingredient_df = pd.DataFrame.sparse.from_spmatrix(ingredient_matrix, columns=f_ingredient_names,
                                                             index=recipe_data.index)
    recipe_data_exp = pd.concat([recipe_data, recipe_ingredient_df], axis=1)

    # Prepare the leftover ingredients as a sparse vector
    leftover_vector = pd.DataFrame.sparse.from_spmatrix(csr_matrix((1, len(f_ingredient_names))),
                                                        columns=f_ingredient_names)
    for ingredient in leftover_ingredients:
        if ingredient in leftover_vector.columns:
            leftover_vector[ingredient] = 1

    # Extract recipe vectors as sparse matrix
    recipe_vectors = ingredient_matrix

    # Calculate cosine similarity between the leftover vector and recipe vectors
    similarity_scores = cosine_similarity(leftover_vector, recipe_vectors)

    # Add similarity scores to the recipe data
    recipe_data_exp['Cosine Similarity Score'] = similarity_scores[0]

    # Prepare the leftover ingredients as a set
    leftover_set = set(leftover_ingredients)

    # Apply the function to calculate the usage percentage for each recipe and store the intersections
    leftover_usage_data = recipe_data_exp['Ingredients'].apply(calculate_leftover_usage, args=(leftover_set,))
    recipe_data_exp['Leftover Usage Percentage'] = leftover_usage_data.apply(lambda x: x[0])
    recipe_data_exp['Ingredient Intersection'] = leftover_usage_data.apply(lambda x: x[1])
    recipe_data_exp['Unused Leftovers'] = leftover_usage_data.apply(lambda x: x[2])
    recipe_data_exp['Ingredients Needed'] = leftover_usage_data.apply(lambda x: x[3])

    # Normalize the scores to the range [0, 1]
    recipe_data_exp['Normalized Cosine Similarity'] = (recipe_data_exp['Cosine Similarity Score'] - recipe_data_exp[
        'Cosine Similarity Score'].min()) / (recipe_data_exp['Cosine Similarity Score'].max() - recipe_data_exp[
        'Cosine Similarity Score'].min())
    recipe_data_exp['Normalized Leftover Usage'] = recipe_data_exp['Leftover Usage Percentage'] / 100

    # Combine the scores with equal weights (50% each)
    recipe_data_exp['Combined Score'] = 0.5 * recipe_data_exp['Normalized Cosine Similarity'] + 0.5 * recipe_data_exp[
        'Normalized Leftover Usage']

    # Sort recipes by the combined score in descending order
    sorted_recipes = recipe_data_exp.sort_values(by='Combined Score', ascending=False)

    # Limit the output to the top 10 recipes
    top_10_recipes = sorted_recipes.head(10)
    return top_10_recipes


# Streamlit app
# Path to your image file
logo_path = "./waste-not-logo.png"
# Open the image using PIL
logo = Image.open(logo_path)
# Display the image using st.image
st.image(logo, caption=None, use_column_width=True)
st.title('Waste Not: Leftover Ingredients Recipe Finder')

# User input for leftover ingredients
st.header('Enter your leftover ingredients:')
ingredient = st.text_input('Type an ingredient').strip().lower()

if st.button('Add to list'):
    if 'leftover_list' not in st.session_state:
        st.session_state.leftover_list = []
    if ingredient and ingredient not in st.session_state.leftover_list:
        st.session_state.leftover_list.append(ingredient)

# Display the ingredients list as markdown bullets
if 'leftover_list' in st.session_state and st.session_state.leftover_list:
    st.write('Your leftover ingredients list:')
    # Loop and render each element
    for item in st.session_state.leftover_list:
        with st.container():
            st.markdown(f"- {item}")
    #ingredient_table = pd.DataFrame(st.session_state.leftover_list, columns=['Ingredients'])
    #st.table(ingredient_table)

if st.button('Find recipes!'):
    if 'leftover_list' in st.session_state:
        leftover_ingredients = st.session_state.leftover_list

        # Calculate cosine similarity scores
        recipe_data_exp = calculate_cosine_similarity(recipe_data, leftover_ingredients)

        # Find top recipes based on combined score
        top_10_recipes = find_top_recipes(recipe_data_exp, leftover_ingredients)

        # Display the top 10 recipes with their combined scores
        st.header('Top 10 Recipes For You:')
        for index, row in top_10_recipes.iterrows():
            with st.expander(f"{row['Recipe Name']}"):
                ingredient_list = row['Ingredients']
                st.write("Ingredients:")
                for ingredient in ingredient_list:
                    st.markdown(f"- {ingredient}")
                st.write(f"Combined Score: {(row['Combined Score'] * 100):.2f} out of 100")
                st.write(f"Cosine Similarity Score: {(row['Cosine Similarity Score'] * 100):.2f}%")
                st.write(f"Leftover Usage Percentage: {row['Leftover Usage Percentage']:.2f}%")
                st.write(f"Ingredients Intersection: {row['Ingredient Intersection']}")
                if row['Unused Leftovers']:
                    st.write(f"Unused Leftovers: {row['Unused Leftovers']}")
                else:
                    st.write(f"Unused Leftovers: None!")
                st.write(f"Ingredients To Buy: {row['Ingredients To Buy']}")
    else:
        st.warning('Please add some leftover ingredients to the list!')
