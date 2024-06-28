import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# Set the maximum number of columns to display
pd.set_option('display.max_columns', 50)

# Load the dataset from CSV file
fdcdf = pd.read_csv('data/RAW_recipes_Food_com.csv')

# Rename columns for consistency
fdcdf.rename(columns={'id': 'Recipe ID', 'name': 'Recipe Name', 'ingredients': 'Ingredients'}, inplace=True)

# Sample a subset of the DataFrame for development
sample_size = 5500  # Small right now to keep the time to run the program shorter
recipe_data = fdcdf.sample(n=sample_size, random_state=42)

# Ensure ingredients are in the correct format
def clean_ingredients(ingredients_str):
    return ingredients_str.lower().replace('[', '').replace('  ', ' ').replace(']', '').replace('\'', '').split(', ')

recipe_data['Ingredients'] = recipe_data['Ingredients'].apply(clean_ingredients)

# Sample leftover ingredients / pantry ingredients
leftover_ingredients = ["onions", "carrots", "rice", "tomato sauce", "mushrooms", "black beans", "tomatoes", "green beans", "chicken"]
leftover_ingredients = [ingredient.lower() for ingredient in leftover_ingredients]

# Use MultiLabelBinarizer with sparse output to one-hot encode the ingredients
mlb = MultiLabelBinarizer(sparse_output=True)
ingredient_matrix = mlb.fit_transform(recipe_data['Ingredients'])
f_ingredient_names = mlb.classes_

# Convert to sparse DataFrame
recipe_ingredient_df = pd.DataFrame.sparse.from_spmatrix(ingredient_matrix, columns=f_ingredient_names, index=recipe_data.index)
recipe_data = pd.concat([recipe_data, recipe_ingredient_df], axis=1)

# Prepare the leftover ingredients as a sparse vector
leftover_vector = pd.DataFrame.sparse.from_spmatrix(csr_matrix((1, len(f_ingredient_names))), columns=f_ingredient_names)
for ingredient in leftover_ingredients:
    if ingredient in leftover_vector.columns:
        leftover_vector[ingredient] = 1

# Extract recipe vectors as sparse matrix
recipe_vectors = ingredient_matrix

# Calculate cosine similarity between the leftover vector and recipe vectors
similarity_scores = cosine_similarity(leftover_vector, recipe_vectors)

# Add similarity scores to the recipe data
recipe_data['Cosine Similarity Score'] = similarity_scores[0]

# Prepare the leftover ingredients as a set
leftover_set = set(leftover_ingredients)

# Function to calculate the percentage of leftover ingredients used in each recipe
def calculate_leftover_usage(ingredients):
    ingredients_set = set(ingredients)
    intersection = ingredients_set.intersection(leftover_set)
    unused_leftovers = leftover_set.difference(ingredients_set)
    ingredients_to_buy = ingredients_set.difference(leftover_set)
    return len(intersection) / len(leftover_set) * 100, intersection, unused_leftovers, ingredients_to_buy

# Apply the function to calculate the usage percentage for each recipe and store the intersections
leftover_usage_data = recipe_data['Ingredients'].apply(calculate_leftover_usage)
recipe_data['Leftover Usage Percentage'] = leftover_usage_data.apply(lambda x: x[0])
recipe_data['Ingredient Intersection'] = leftover_usage_data.apply(lambda x: x[1])
recipe_data['Unused Leftovers'] = leftover_usage_data.apply(lambda x: x[2])
recipe_data['Ingredients Needed'] = leftover_usage_data.apply(lambda x: x[3])


# Normalize the scores to the range [0, 1]
recipe_data['Normalized Cosine Similarity'] = (recipe_data['Cosine Similarity Score'] - recipe_data['Cosine Similarity Score'].min()) / (recipe_data['Cosine Similarity Score'].max() - recipe_data['Cosine Similarity Score'].min())
recipe_data['Normalized Leftover Usage'] = recipe_data['Leftover Usage Percentage'] / 100

# Combine the scores with equal weights (50% each)
recipe_data['Combined Score'] = 0.5 * recipe_data['Normalized Cosine Similarity'] + 0.5 * recipe_data['Normalized Leftover Usage']

# Sort recipes by the combined score in descending order
sorted_recipes = recipe_data.sort_values(by='Combined Score', ascending=False)

# Limit the output to the top 10 recipes
top_10_recipes = sorted_recipes.head(10)

# Display the top 10 recipes with their combined scores
print("Your leftover ingredients input: ")
print(leftover_set)
print("\nTop 10 recipes sorted by combined score:")
print(top_10_recipes[['Recipe ID', 'Recipe Name', 'Ingredients', 'Combined Score', 'Cosine Similarity Score', 'Leftover Usage Percentage', 'Ingredient Intersection', 'Unused Leftovers', 'Ingredients Needed']])
